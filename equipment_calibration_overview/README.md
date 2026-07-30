<!-- ####
  - AI MODIFIED FILE
  - Filename: `README.md`
  - Modified (date/time): `2026-07-30 14:24:08 +02:00 (Romance Standard Time)`
  - Modified by: `Cursor AI Assistant (commanded by JonathanVandenBerk)`
  - License: `Internal - Magics Technologies`
  - Version: `1.0.0`
  - Description: New file. Usage documentation for the calibration overview script.
#### -->

# Equipment calibration overview per product tester

Generates an overview of the **calibration end date** of every instrument used by a
product test system, based on the lab equipment list.

- **Input**: `List_Of_Equipment.xlsm`, sheet `Equipment`
  (default path: `%USERPROFILE%\Magics Technologies\Lab - Labo Equipment\List_Of_Equipment.xlsm`)
- **Input**: [`tester_equipment.json`](tester_equipment.json) — which equipment belongs to which tester
- **Output**: `output/calibration_overview.html`, `output/calibration_overview.xlsx` and a console table

## Colour coding

| Colour | Status | Meaning |
|---|---|---|
| 🔴 red | Out of calibration | `Calibration Valid until` is in the past |
| 🟠 orange | Expires within warning window | expires within `warn_days` (default **30 days**) |
| 🟢 green | In calibration | calibration valid |
| ⚪ grey | No calibration required | `Calibration strategy` = *No calibration needed*, or `"calibration_required": false` in the config |
| 🟣 purple | No calibration date | a calibration strategy is defined but there is no valid-until date |
| 🟡 yellow | Not found in equipment list | the label is not present in the `Equipment` sheet — fix the config or the lab list |

## Run

```bash
python calibration_overview.py
```

Useful options:

```bash
python calibration_overview.py --open --warn-days 60 --tester CXP00002
```

| Option | Description |
|---|---|
| `--xlsm PATH` | other input workbook |
| `--sheet NAME` | other sheet name (default `Equipment`) |
| `--config PATH` | other tester/equipment mapping |
| `--outdir PATH` | other output folder (default `./output`) |
| `--warn-days N` | orange warning window in days (default: `warn_days` from the config, else 30) |
| `--today YYYY-MM-DD` | evaluate against another reference date (useful to look ahead) |
| `--tester TEXT` | only report test systems whose name contains `TEXT` |
| `--no-html` / `--no-xlsx` | skip an output format |
| `--open` | open the HTML report in the browser |

Exit code is `1` when at least one instrument needs attention (expired, expiring,
missing date, unknown label) and `0` when everything is fine — so the script can be used
directly as a check in a scheduled task.

## Adding or changing equipment

Everything is data-driven; edit [`tester_equipment.json`](tester_equipment.json) only:

```json
{
  "tester": "IMG002x1 test system",
  "product": "MAG-IMG002x1-NC",
  "equipment": [
    { "name": "Power Supply Unit", "label": "PSU16", "type": "R&S NGL202" }
  ]
}
```

- `label` must match the **Label** column of the `Equipment` sheet. Matching ignores
  case, spaces, underscores and dashes, so `Scope 6` matches `SCOPE6`.
- If the tester documentation uses another label than the lab list, add an entry to
  `label_aliases` (e.g. `"THERMO1": "TEMP3"`).
- Add `"calibration_required": false` for items that are not calibrated instruments
  (dev boards, adapters, ...). They are listed but never coloured red or orange.
- Equipment shared between testers (e.g. the thermostreamer) is simply listed in both
  testers.

## Current state

All three IC test systems are configured: **PSU00001**, **CXP00002** and **IMG002x1**.
The thermostreamer (`TEMP3`, Temptronic ECO-710E-M) is shared between the PSU00001 and
CXP00002 test systems.

## Which revision of the equipment list is used?

The workbook is re-read from disk on **every** run — nothing is cached and no copy is
kept. Every output (console, HTML, Excel) shows the **last-saved timestamp** of
`List_Of_Equipment.xlsm` so you can see which revision the overview was built from.

Two things to keep in mind:

- **Open in Excel**: the script reads the file in shared mode and reports the *last
  saved* content (it prints a note). Save in Excel first after editing a date.
- **OneDrive**: you get whatever your locally synced copy contains. If a colleague saved
  a newer version in the cloud and sync has not pulled it down yet, the overview is
  based on the older local revision.
- The `Calibration Valid until` column is a formula (`=<last calibration>+365`, `+3*365`,
  `+5*365`) in most rows. The script reads the value Excel cached for that formula, i.e.
  exactly what Excel shows. A row whose formula has no cached value shows up as
  🟣 *No calibration date* instead of being reported incorrectly.

## Notes

- `--today` lets you look ahead, e.g. `--today 2026-09-01` shows what will be out of
  calibration at the start of September.
