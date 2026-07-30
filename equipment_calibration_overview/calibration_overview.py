# ####
# - AI MODIFIED FILE
# - Filename: `calibration_overview.py`
# - Modified (date/time): `2026-07-30 14:24:08 +02:00 (Romance Standard Time)`
# - Modified by: `Cursor AI Assistant (commanded by JonathanVandenBerk)`
# - License: `Internal - Magics Technologies`
# - Version: `1.2.0`
# - Description: Reads the Equipment sheet of List_Of_Equipment.xlsm and generates a
#   calibration end-date overview per product tester (HTML + Excel + console),
#   highlighting out-of-calibration equipment in red and equipment expiring within the
#   warning window (default 1 month) in orange. v1.1.0: read the workbook in shared mode
#   when it is open in Excel, and do not show an action verdict for empty test systems.
#   v1.2.0: report the last-saved timestamp of the source workbook in every output.
# ####
"""Calibration overview per product tester.

Input : List_Of_Equipment.xlsm  (sheet 'Equipment')  +  tester_equipment.json
Output: calibration_overview.html / .xlsx  (+ console summary)

Usage:
    python calibration_overview.py
    python calibration_overview.py --tester CXP00002
    python calibration_overview.py --warn-days 60 --open
"""

from __future__ import annotations

import argparse
import ctypes
import io
import json
import os
import sys
import webbrowser
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

# =========================================================================
# Settings (edit defaults)
# =========================================================================
SCRIPT_DIR = Path(__file__).resolve().parent

# Input workbook. The lab list lives in the OneDrive/SharePoint synced folder.
DEFAULT_XLSM_PATH = Path(
    os.path.expandvars(
        r"%USERPROFILE%\Magics Technologies\Lab - Labo Equipment\List_Of_Equipment.xlsm"
    )
)
DEFAULT_SHEET_NAME = "Equipment"

# Tester -> equipment mapping (see tester_equipment.json for the format).
DEFAULT_CONFIG_PATH = SCRIPT_DIR / "tester_equipment.json"

# Outputs.
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "output"
DEFAULT_HTML_NAME = "calibration_overview.html"
DEFAULT_XLSX_NAME = "calibration_overview.xlsx"
WRITE_HTML = True
WRITE_XLSX = True
OPEN_HTML_AFTER_WRITE = False

# Equipment expiring within this many days is flagged orange ("1 month" by default).
DEFAULT_WARN_DAYS = 30

# Values in the calibration columns that mean "no calibration date on record".
NO_DATE_TOKENS = {"", "/", "na", "n.a.", "n/a", "-", "none", "no", "nvt"}
# Calibration strategy values that mean the equipment is not calibrated at all.
NO_CAL_STRATEGY_TOKENS = {"no calibration needed", "na", "n.a.", "/"}

# Colour scheme (HTML hex / Excel ARGB) per status.
STATUS_STYLE = {
    # status        label                        html bg    html text  xlsx fill
    "EXPIRED":     ("Out of calibration",        "#f8c9c4", "#8e1b0f", "FFF8C9C4"),
    "DUE_SOON":    ("Expires within warning",    "#ffd9a8", "#8a4b00", "FFFFD9A8"),
    "OK":          ("In calibration",            "#d9efd2", "#1f5c2e", "FFD9EFD2"),
    "NO_CAL_REQ":  ("No calibration required",   "#e9e9e9", "#5a5a5a", "FFE9E9E9"),
    "NO_DATE":     ("No calibration date",       "#e2d7f0", "#4b2d73", "FFE2D7F0"),
    "NOT_FOUND":   ("Not found in equipment list", "#ffe9a8", "#7a5c00", "FFFFE9A8"),
}
# Order used for sorting / summary counters (most urgent first).
STATUS_ORDER = ["EXPIRED", "DUE_SOON", "NO_DATE", "NOT_FOUND", "OK", "NO_CAL_REQ"]

# Expected header names in the Equipment sheet (matched case-insensitively,
# a header only has to *start with* the text below).
HEADER_KEYS = {
    "name": "name",
    "manufacturer": "manufacturer",
    "type": "type",
    "label": "label",
    "serial": "serial number",
    "last_cal": "last calibration date",
    "valid_until": "calibration valid until",
    "strategy": "calibration strategy",
    "service": "calibration service",
    "comment": "comment",
}


# =========================================================================
# Data model
# =========================================================================
@dataclass
class EquipmentRecord:
    """One calibrated instrument as listed in the Equipment sheet."""

    row: int
    category: str = ""
    name: str = ""
    manufacturer: str = ""
    type: str = ""
    label: str = ""
    serial: str = ""
    last_cal: date | None = None
    valid_until: date | None = None
    valid_until_raw: str = ""
    strategy: str = ""
    service: str = ""
    comment: str = ""


@dataclass
class OverviewRow:
    """One line of the report: a tester's equipment entry joined with the lab list."""

    tester: str
    name: str
    label: str
    type: str
    status: str
    record: EquipmentRecord | None = None
    days_left: int | None = None
    note: str = ""

    @property
    def status_label(self) -> str:
        return STATUS_STYLE[self.status][0]

    @property
    def valid_until_text(self) -> str:
        if self.record is None:
            return "-"
        if self.record.valid_until is not None:
            return self.record.valid_until.isoformat()
        return self.record.valid_until_raw or "-"

    @property
    def last_cal_text(self) -> str:
        if self.record is None or self.record.last_cal is None:
            return "-"
        return self.record.last_cal.isoformat()

    @property
    def days_left_text(self) -> str:
        if self.days_left is None:
            return "-"
        if self.days_left < 0:
            return f"{-self.days_left} days overdue"
        return f"{self.days_left} days"


@dataclass
class TesterOverview:
    """All equipment of a single product tester."""

    tester: str
    product: str = ""
    note: str = ""
    rows: list[OverviewRow] = field(default_factory=list)

    def count(self, status: str) -> int:
        return sum(1 for r in self.rows if r.status == status)

    @property
    def worst_status(self) -> str:
        for status in STATUS_ORDER:
            if self.count(status):
                return status
        return "OK"


# =========================================================================
# Helpers
# =========================================================================
def norm_label(value: Any) -> str:
    """Normalise a label so 'Scope 6', 'scope_6' and 'SCOPE6' all match."""
    return str(value or "").strip().upper().replace(" ", "").replace("_", "").replace("-", "")


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value).strip()


def as_date(value: Any) -> date | None:
    """Convert an Excel cell value to a date, or None when it is not a date."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = as_text(value)
    if text.lower() in NO_DATE_TOKENS:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y", "%d.%m.%Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def is_no_cal_strategy(strategy: str) -> bool:
    return strategy.strip().lower() in NO_CAL_STRATEGY_TOKENS


def file_revision(path: Path) -> str:
    """Last-modified timestamp of the input workbook, so the report shows which
    revision of the equipment list it was built from."""
    try:
        return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    except OSError:
        return "unknown"


def read_locked_file(path: Path) -> bytes:
    """Read a file that is locked by another application (Windows).

    Excel opens the equipment list with a lock that Python's open() cannot pass, so the
    file is opened through CreateFileW with all sharing flags set. Returns the bytes of
    the file as last saved on disk.
    """
    if os.name != "nt":
        raise SystemExit(f"ERROR: cannot read {path} - the file is locked.")

    generic_read = 0x80000000
    share_all = 0x1 | 0x2 | 0x4  # read | write | delete
    open_existing = 3
    invalid_handle = ctypes.c_void_p(-1).value

    kernel32 = ctypes.windll.kernel32
    kernel32.CreateFileW.restype = ctypes.c_void_p
    kernel32.CreateFileW.argtypes = [
        ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32,
        ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p,
    ]
    handle = kernel32.CreateFileW(
        str(path), generic_read, share_all, None, open_existing, 0, None
    )
    if not handle or handle == invalid_handle:
        raise SystemExit(
            f"ERROR: cannot read {path} (Windows error {ctypes.get_last_error()}). "
            "Close the workbook in Excel and run again."
        )
    try:
        buffer = ctypes.create_string_buffer(1 << 20)
        bytes_read = ctypes.c_uint32(0)
        chunks: list[bytes] = []
        while True:
            if not kernel32.ReadFile(
                ctypes.c_void_p(handle), buffer, len(buffer),
                ctypes.byref(bytes_read), None
            ):
                raise SystemExit(f"ERROR: reading {path} failed.")
            if bytes_read.value == 0:
                break
            chunks.append(buffer.raw[: bytes_read.value])
        return b"".join(chunks)
    finally:
        kernel32.CloseHandle(ctypes.c_void_p(handle))


# =========================================================================
# Reading the Equipment sheet
# =========================================================================
def find_header_columns(worksheet) -> dict[str, int]:
    """Locate the column index of every known header in the first rows."""
    columns: dict[str, int] = {}
    for row in range(1, min(11, worksheet.max_row + 1)):
        for col in range(1, worksheet.max_column + 1):
            cell_text = as_text(worksheet.cell(row, col).value).lower()
            if not cell_text:
                continue
            for key, expected in HEADER_KEYS.items():
                if key not in columns and cell_text.startswith(expected):
                    columns[key] = col
        if "label" in columns and "valid_until" in columns:
            columns["_header_row"] = row
            break
    missing = [k for k in ("label", "valid_until") if k not in columns]
    if missing:
        raise SystemExit(
            f"ERROR: could not find the column(s) {missing} in sheet '{worksheet.title}'. "
            "Has the layout of List_Of_Equipment.xlsm changed?"
        )
    return columns


def read_equipment(xlsm_path: Path, sheet_name: str) -> dict[str, EquipmentRecord]:
    """Return {normalised label: EquipmentRecord} for the whole Equipment sheet."""
    if not xlsm_path.is_file():
        raise SystemExit(f"ERROR: input workbook not found: {xlsm_path}")

    try:
        workbook = openpyxl.load_workbook(xlsm_path, data_only=True, read_only=False)
    except PermissionError:
        # Excel keeps the workbook open with a lock that plain open() cannot pass.
        # Read it through a shared handle instead of asking the user to close Excel.
        print(f"NOTE: {xlsm_path.name} is open in Excel - reading it in shared mode "
              "(unsaved changes are not included).")
        workbook = openpyxl.load_workbook(
            io.BytesIO(read_locked_file(xlsm_path)), data_only=True, read_only=False
        )

    if sheet_name not in workbook.sheetnames:
        raise SystemExit(
            f"ERROR: sheet '{sheet_name}' not found in {xlsm_path.name}. "
            f"Available sheets: {workbook.sheetnames}"
        )
    worksheet = workbook[sheet_name]
    columns = find_header_columns(worksheet)
    header_row = columns.get("_header_row", 1)

    def cell(row: int, key: str) -> Any:
        col = columns.get(key)
        return worksheet.cell(row, col).value if col else None

    records: dict[str, EquipmentRecord] = {}
    category = ""
    for row in range(header_row + 1, worksheet.max_row + 1):
        name = as_text(cell(row, "name"))
        label = as_text(cell(row, "label"))
        type_text = as_text(cell(row, "type"))
        valid_raw = cell(row, "valid_until")

        # Category header rows only carry a name (e.g. 'Power Supply', "Scope's").
        if name and not label and not type_text and valid_raw in (None, ""):
            category = name
            continue
        if not label and not name:
            continue

        record = EquipmentRecord(
            row=row,
            category=category,
            name=name,
            manufacturer=as_text(cell(row, "manufacturer")),
            type=type_text,
            label=label,
            serial=as_text(cell(row, "serial")),
            last_cal=as_date(cell(row, "last_cal")),
            valid_until=as_date(valid_raw),
            valid_until_raw=as_text(valid_raw),
            strategy=as_text(cell(row, "strategy")),
            service=as_text(cell(row, "service")),
            comment=as_text(cell(row, "comment")),
        )
        key = norm_label(label)
        if key and key not in records:
            records[key] = record
    workbook.close()
    return records


# =========================================================================
# Status evaluation
# =========================================================================
def evaluate(
    entry: dict[str, Any],
    tester: str,
    records: dict[str, EquipmentRecord],
    aliases: dict[str, str],
    today: date,
    warn_days: int,
) -> OverviewRow:
    """Join one config entry with the lab list and determine its status."""
    label = as_text(entry.get("label"))
    name = as_text(entry.get("name"))
    type_text = as_text(entry.get("type"))
    note = as_text(entry.get("note"))
    cal_required = bool(entry.get("calibration_required", True))

    key = norm_label(label)
    key = norm_label(aliases.get(key, key))
    record = records.get(key)

    if not cal_required:
        return OverviewRow(tester, name, label, type_text, "NO_CAL_REQ", record, None, note)
    if record is None:
        return OverviewRow(tester, name, label, type_text, "NOT_FOUND", None, None, note)

    type_text = type_text or record.type
    name = name or record.name

    if record.valid_until is None:
        status = "NO_CAL_REQ" if is_no_cal_strategy(record.strategy) else "NO_DATE"
        return OverviewRow(tester, name, label, type_text, status, record, None, note)

    days_left = (record.valid_until - today).days
    if is_no_cal_strategy(record.strategy):
        # Equipment that is not calibrated on purpose: report, but never flag.
        status = "NO_CAL_REQ"
    elif days_left < 0:
        status = "EXPIRED"
    elif days_left <= warn_days:
        status = "DUE_SOON"
    else:
        status = "OK"
    return OverviewRow(tester, name, label, type_text, status, record, days_left, note)


def build_overviews(
    config: dict[str, Any],
    records: dict[str, EquipmentRecord],
    today: date,
    warn_days: int,
    tester_filter: str | None,
) -> list[TesterOverview]:
    aliases = {
        norm_label(k): v
        for k, v in (config.get("label_aliases") or {}).items()
        if not k.startswith("_")
    }
    overviews: list[TesterOverview] = []
    for tester_cfg in config.get("testers", []):
        tester = as_text(tester_cfg.get("tester"))
        if tester_filter and tester_filter.lower() not in tester.lower():
            continue
        overview = TesterOverview(
            tester=tester,
            product=as_text(tester_cfg.get("product")),
            note=as_text(tester_cfg.get("note")),
        )
        for entry in tester_cfg.get("equipment", []):
            overview.rows.append(
                evaluate(entry, tester, records, aliases, today, warn_days)
            )
        overview.rows.sort(key=lambda r: (STATUS_ORDER.index(r.status), r.label))
        overviews.append(overview)
    return overviews


# =========================================================================
# Console output
# =========================================================================
def print_console(
    overviews: list[TesterOverview], today: date, warn_days: int, xlsm_path: Path
) -> None:
    print()
    print("=" * 96)
    print(f"Equipment calibration overview per product tester   (reference date: {today})")
    print(f"Warning window: {warn_days} days")
    print(f"Source: {xlsm_path.name}, last saved {file_revision(xlsm_path)}")
    print("=" * 96)
    for overview in overviews:
        title = overview.tester + (f"  [{overview.product}]" if overview.product else "")
        print(f"\n{title}")
        print("-" * len(title))
        if not overview.rows:
            print("  (no equipment defined in tester_equipment.json)")
            if overview.note:
                print(f"  note: {overview.note}")
            continue
        print(
            f"  {'Label':<10} {'Equipment':<28} {'Type':<22} "
            f"{'Valid until':<12} {'Remaining':<18} Status"
        )
        for row in overview.rows:
            marker = {"EXPIRED": "!!", "DUE_SOON": " !"}.get(row.status, "  ")
            print(
                f"{marker}{row.label:<10} {row.name[:28]:<28} {row.type[:22]:<22} "
                f"{row.valid_until_text:<12} {row.days_left_text:<18} {row.status_label}"
            )
        counts = ", ".join(
            f"{STATUS_STYLE[s][0]}: {overview.count(s)}"
            for s in STATUS_ORDER
            if overview.count(s)
        )
        print(f"  -> {counts}")
    print()


# =========================================================================
# HTML output
# =========================================================================
def esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def html_report(
    overviews: list[TesterOverview],
    today: date,
    warn_days: int,
    xlsm_path: Path,
) -> str:
    parts: list[str] = []
    parts.append(
        f"""<!-- ####
  - AI GENERATED FILE
  - Filename: `{DEFAULT_HTML_NAME}`
  - Generated (date/time): `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`
  - Generated by: `calibration_overview.py`
  - License: `Internal - Magics Technologies`
  - Version: `1.0.0`
  - Description: Calibration end-date overview per product tester.
#### -->
<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Equipment calibration overview per product tester</title>
<style>
  body {{ font-family: Segoe UI, Arial, sans-serif; margin: 24px; color: #202020; }}
  h1 {{ font-size: 22px; margin-bottom: 4px; }}
  h2 {{ font-size: 17px; margin-top: 30px; border-bottom: 2px solid #d8d8d8;
        padding-bottom: 4px; }}
  .meta {{ color: #666; font-size: 12px; margin-bottom: 18px; }}
  table {{ border-collapse: collapse; width: 100%; max-width: 1200px;
           font-size: 13px; margin-top: 8px; }}
  th {{ background: #e8322a; color: #fff; text-align: left; padding: 6px 8px;
        font-weight: 600; }}
  td {{ padding: 5px 8px; border-bottom: 1px solid #e5e5e5; vertical-align: top; }}
  .legend span {{ display: inline-block; padding: 3px 10px; margin-right: 8px;
                  border-radius: 3px; font-size: 12px; }}
  .badge {{ display: inline-block; padding: 1px 8px; border-radius: 10px;
            font-size: 11px; font-weight: 600; }}
  .note {{ color: #666; font-style: italic; font-size: 12px; }}
  .summary td, .summary th {{ font-size: 13px; }}
</style></head><body>
<h1>Equipment calibration overview per product tester</h1>
<div class="meta">
  Reference date: <b>{today.isoformat()}</b> &nbsp;|&nbsp;
  Warning window: <b>{warn_days} days</b> &nbsp;|&nbsp;
  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}<br>
  Source: {esc(str(xlsm_path))} (sheet '{DEFAULT_SHEET_NAME}'),
  last saved <b>{file_revision(xlsm_path)}</b>
</div>
<div class="legend">"""
    )
    for status in STATUS_ORDER:
        label, bg, fg, _ = STATUS_STYLE[status]
        parts.append(
            f'<span style="background:{bg};color:{fg}">{esc(label)}</span>'
        )
    parts.append("</div>")

    # ---- summary per tester -------------------------------------------------
    parts.append("<h2>Summary</h2><table class='summary'><tr><th>Test system</th>"
                 "<th>Product</th><th>Equipment</th>")
    for status in STATUS_ORDER:
        parts.append(f"<th>{esc(STATUS_STYLE[status][0])}</th>")
    parts.append("<th>Action needed</th></tr>")
    for overview in overviews:
        worst = overview.worst_status
        label, bg, fg, _ = STATUS_STYLE[worst]
        action = "yes" if worst in ("EXPIRED", "DUE_SOON", "NO_DATE", "NOT_FOUND") else "no"
        parts.append(
            f"<tr><td><b>{esc(overview.tester)}</b></td><td>{esc(overview.product)}</td>"
            f"<td>{len(overview.rows)}</td>"
        )
        for status in STATUS_ORDER:
            count = overview.count(status)
            cell_bg = STATUS_STYLE[status][1] if count else "transparent"
            cell_fg = STATUS_STYLE[status][2] if count else "#999"
            parts.append(
                f'<td style="background:{cell_bg};color:{cell_fg};text-align:center">'
                f"{count or '-'}</td>"
            )
        if overview.rows:
            parts.append(
                f'<td><span class="badge" style="background:{bg};color:{fg}">'
                f"{action} ({esc(label)})</span></td></tr>"
            )
        else:
            parts.append('<td class="note">no equipment defined</td></tr>')
    parts.append("</table>")

    # ---- one table per tester ----------------------------------------------
    for overview in overviews:
        title = overview.tester
        if overview.product:
            title += f" &ndash; {esc(overview.product)}"
        parts.append(f"<h2>{title}</h2>")
        if overview.note:
            parts.append(f'<div class="note">{esc(overview.note)}</div>')
        if not overview.rows:
            parts.append('<div class="note">No equipment defined in '
                         "tester_equipment.json.</div>")
            continue
        parts.append(
            "<table><tr><th>Label</th><th>Equipment name</th><th>Type</th>"
            "<th>Serial number</th><th>Last calibration</th>"
            "<th>Calibration valid until</th><th>Remaining</th>"
            "<th>Calibration strategy</th><th>Service</th><th>Status</th></tr>"
        )
        for row in overview.rows:
            _, bg, fg, _ = STATUS_STYLE[row.status]
            rec = row.record
            note_html = (
                f'<br><span class="note">{esc(row.note)}</span>' if row.note else ""
            )
            parts.append(
                f'<tr style="background:{bg};color:{fg}">'
                f"<td><b>{esc(row.label)}</b></td>"
                f"<td>{esc(row.name)}{note_html}</td>"
                f"<td>{esc(row.type)}</td>"
                f"<td>{esc(rec.serial if rec else '-')}</td>"
                f"<td>{esc(row.last_cal_text)}</td>"
                f"<td><b>{esc(row.valid_until_text)}</b></td>"
                f"<td>{esc(row.days_left_text)}</td>"
                f"<td>{esc(rec.strategy if rec else '-')}</td>"
                f"<td>{esc(rec.service if rec else '-')}</td>"
                f"<td>{esc(row.status_label)}</td></tr>"
            )
        parts.append("</table>")

    # ---- action list: everything that needs attention ----------------------
    attention = [
        row
        for overview in overviews
        for row in overview.rows
        if row.status in ("EXPIRED", "DUE_SOON", "NO_DATE", "NOT_FOUND")
    ]
    parts.append("<h2>Action list</h2>")
    if not attention:
        parts.append('<div class="note">All calibrated equipment of the listed test '
                     "systems is within its calibration window.</div>")
    else:
        attention.sort(
            key=lambda r: (STATUS_ORDER.index(r.status), r.days_left is None, r.days_left or 0)
        )
        parts.append(
            "<table><tr><th>Status</th><th>Test system</th><th>Label</th>"
            "<th>Equipment</th><th>Valid until</th><th>Remaining</th></tr>"
        )
        for row in attention:
            label, bg, fg, _ = STATUS_STYLE[row.status]
            parts.append(
                f'<tr style="background:{bg};color:{fg}"><td>{esc(label)}</td>'
                f"<td>{esc(row.tester)}</td><td><b>{esc(row.label)}</b></td>"
                f"<td>{esc(row.name)} ({esc(row.type)})</td>"
                f"<td><b>{esc(row.valid_until_text)}</b></td>"
                f"<td>{esc(row.days_left_text)}</td></tr>"
            )
        parts.append("</table>")

    parts.append("</body></html>")
    return "\n".join(parts)


# =========================================================================
# Excel output
# =========================================================================
XLSX_HEADERS = [
    "Test system",
    "Label",
    "Equipment name",
    "Type",
    "Serial number",
    "Last calibration",
    "Calibration valid until",
    "Remaining (days)",
    "Calibration strategy",
    "Calibration service",
    "Status",
    "Note",
]


def xlsx_report(
    overviews: list[TesterOverview],
    today: date,
    warn_days: int,
    out_path: Path,
    xlsm_path: Path,
) -> None:
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Calibration overview"

    thin = Side(style="thin", color="FFD0D0D0")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    header_fill = PatternFill("solid", fgColor="FFE8322A")

    worksheet["A1"] = "Equipment calibration overview per product tester"
    worksheet["A1"].font = Font(bold=True, size=14)
    worksheet["A2"] = (
        f"Reference date: {today.isoformat()}   |   warning window: {warn_days} days   |   "
        f"generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}   |   "
        f"source: {xlsm_path.name}, last saved {file_revision(xlsm_path)}"
    )
    worksheet["A2"].font = Font(italic=True, color="FF666666")

    row_idx = 4
    for col_idx, header in enumerate(XLSX_HEADERS, start=1):
        cell = worksheet.cell(row_idx, col_idx, header)
        cell.font = Font(bold=True, color="FFFFFFFF")
        cell.fill = header_fill
        cell.border = border
        cell.alignment = Alignment(vertical="center")
    header_row_idx = row_idx
    row_idx += 1

    for overview in overviews:
        if not overview.rows:
            cell = worksheet.cell(row_idx, 1, overview.tester)
            cell.font = Font(bold=True)
            worksheet.cell(
                row_idx, 3, overview.note or "no equipment defined"
            ).font = Font(italic=True, color="FF666666")
            row_idx += 1
            continue
        for row in overview.rows:
            rec = row.record
            fill = PatternFill("solid", fgColor=STATUS_STYLE[row.status][3])
            values = [
                overview.tester,
                row.label,
                row.name,
                row.type,
                rec.serial if rec else "",
                rec.last_cal if rec and rec.last_cal else row.last_cal_text,
                rec.valid_until if rec and rec.valid_until else row.valid_until_text,
                row.days_left if row.days_left is not None else "",
                rec.strategy if rec else "",
                rec.service if rec else "",
                row.status_label,
                row.note,
            ]
            for col_idx, value in enumerate(values, start=1):
                cell = worksheet.cell(row_idx, col_idx, value)
                cell.fill = fill
                cell.border = border
                if isinstance(value, date):
                    cell.number_format = "yyyy-mm-dd"
            row_idx += 1
        row_idx += 1  # blank separator line between test systems

    widths = [24, 10, 30, 22, 18, 16, 20, 16, 34, 12, 26, 40]
    for col_idx, width in enumerate(widths, start=1):
        worksheet.column_dimensions[get_column_letter(col_idx)].width = width
    worksheet.freeze_panes = worksheet.cell(header_row_idx + 1, 1)
    worksheet.auto_filter.ref = (
        f"A{header_row_idx}:{get_column_letter(len(XLSX_HEADERS))}{row_idx - 1}"
    )

    # Legend sheet so the colours stay self-explanatory in Excel.
    legend = workbook.create_sheet("Legend")
    legend["A1"] = "Status"
    legend["B1"] = "Meaning"
    for cell in (legend["A1"], legend["B1"]):
        cell.font = Font(bold=True, color="FFFFFFFF")
        cell.fill = header_fill
    meanings = {
        "EXPIRED": "Calibration valid-until date is in the past - do not use for "
                   "production testing until recalibrated.",
        "DUE_SOON": f"Calibration expires within {warn_days} days - plan recalibration.",
        "OK": "Calibration valid.",
        "NO_CAL_REQ": "Calibration strategy is 'No calibration needed' or the item is "
                      "not calibrated equipment.",
        "NO_DATE": "No calibration valid-until date on record while a calibration "
                   "strategy is defined.",
        "NOT_FOUND": "Label not found in the Equipment sheet - check "
                     "tester_equipment.json or the lab list.",
    }
    for offset, status in enumerate(STATUS_ORDER, start=2):
        legend.cell(offset, 1, STATUS_STYLE[status][0]).fill = PatternFill(
            "solid", fgColor=STATUS_STYLE[status][3]
        )
        legend.cell(offset, 2, meanings[status])
    legend.column_dimensions["A"].width = 30
    legend.column_dimensions["B"].width = 90

    workbook.save(out_path)


# =========================================================================
# Main
# =========================================================================
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a calibration end-date overview per product tester."
    )
    parser.add_argument("--xlsm", type=Path, default=DEFAULT_XLSM_PATH,
                        help=f"input workbook (default: {DEFAULT_XLSM_PATH})")
    parser.add_argument("--sheet", default=DEFAULT_SHEET_NAME,
                        help=f"sheet name (default: {DEFAULT_SHEET_NAME})")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH,
                        help="tester -> equipment mapping (JSON)")
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTPUT_DIR,
                        help="output directory")
    parser.add_argument("--warn-days", type=int, default=None,
                        help=f"orange warning window in days "
                             f"(default: config 'warn_days' or {DEFAULT_WARN_DAYS})")
    parser.add_argument("--today", default=None,
                        help="reference date YYYY-MM-DD (default: today)")
    parser.add_argument("--tester", default=None,
                        help="only report test systems whose name contains this text")
    parser.add_argument("--no-html", action="store_true", help="skip the HTML report")
    parser.add_argument("--no-xlsx", action="store_true", help="skip the Excel report")
    parser.add_argument("--open", action="store_true",
                        help="open the HTML report in the default browser")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if not args.config.is_file():
        print(f"ERROR: config file not found: {args.config}", file=sys.stderr)
        return 2
    config = json.loads(args.config.read_text(encoding="utf-8"))

    warn_days = args.warn_days
    if warn_days is None:
        warn_days = int(config.get("warn_days", DEFAULT_WARN_DAYS))
    today = date.today() if args.today is None else as_date(args.today)
    if today is None:
        print(f"ERROR: could not parse --today '{args.today}' (use YYYY-MM-DD)",
              file=sys.stderr)
        return 2

    records = read_equipment(args.xlsm, args.sheet)
    print(f"Read {len(records)} labelled instruments from {args.xlsm.name}")

    overviews = build_overviews(config, records, today, warn_days, args.tester)
    if not overviews:
        print("No test systems matched - check --tester / the config file.")
        return 1

    print_console(overviews, today, warn_days, args.xlsm)

    args.outdir.mkdir(parents=True, exist_ok=True)
    html_path = args.outdir / DEFAULT_HTML_NAME
    xlsx_path = args.outdir / DEFAULT_XLSX_NAME

    if WRITE_HTML and not args.no_html:
        html_path.write_text(
            html_report(overviews, today, warn_days, args.xlsm), encoding="utf-8"
        )
        print(f"HTML report : {html_path}")
        if args.open or OPEN_HTML_AFTER_WRITE:
            webbrowser.open(html_path.as_uri())
    if WRITE_XLSX and not args.no_xlsx:
        try:
            xlsx_report(overviews, today, warn_days, xlsx_path, args.xlsm)
            print(f"Excel report: {xlsx_path}")
        except PermissionError:
            print(f"WARNING: could not write {xlsx_path} - close the file in Excel "
                  "and run again.", file=sys.stderr)

    # Exit code 1 when something needs attention, so the script can be used in CI /
    # scheduled tasks as a check.
    needs_action = any(
        overview.count(status)
        for overview in overviews
        for status in ("EXPIRED", "DUE_SOON", "NO_DATE", "NOT_FOUND")
    )
    return 1 if needs_action else 0


if __name__ == "__main__":
    sys.exit(main())
