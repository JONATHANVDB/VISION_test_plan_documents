# Vision Series Test Plan Document

## 1. Revision History

| Revision | Date | Description | Author |
| :--- | :--- | :--- | :--- |
| 1.0 | 2026-04-10 | Initial draft of the Vision Series Test Plan | Test Architect |
| 1.1 | 2026-04-13 | Updated diagrams and test stage descriptions | Test Architect |

## 2. List of Figures

- Figure 1: Vision Series: three-step verification rail
- Figure 2: MAG-IMG002x1-NC Production Test Flow
- Figure 3: MAG-IMG002x1-NC Trim Test Flow
- Figure 4: MAG-CXP00002-NP Production Test Flow
- Figure 5: MAG-PSU00001-NP Production Test Flow
- Figure 6: MAG-VIS4000x-N Production Test Flow
- Figure 7: MAG-VIS4003x-N Production Test Flow
- Figure 8: MAG-VIS4001x-N Production Test Flow
- Figure 9: MAG-VIS100xx-N Production Test Flow

## 3. List of Tables

- Table 1: MAG-IMG002X1-NC Key Specifications
- Table 2: MAG-CXP00002-NP Key Specifications
- Table 3: MAG-PSU00001-NP Key Specifications
- Table 4: MAG-VIS100xx-N Key Specifications

---

## 4. Introduction & Scope

This document outlines the verification for the Magics Technologies Vision Series products to ensure suitability for nuclear environments. The Vision Series includes standalone radiation-hardened ICs (Image Sensor, Serializer, DC/DC Converter) and fully integrated electronic Vision Modules.

This test plan details the test conditions, test flows, test stages, and the production and trimming tests required to guarantee the reliability and performance of the products.

---

## 5. Vision products verification process

The verification and testing of the Vision Series products follow a three-step horizontal process rail. This ensures that quality is maintained incrementally from the IC component level up to the fully integrated module. While testing a MAG-VIS100xx product spans from component to module, our verification is gated: customers purchasing IC-only or PCB products receive components that have successfully cleared the specific segments of the rail required for those tiers.

![Vision Series: three-step verification rail](vision-module-testing-diagrams/diagram-1-option-c-process-rail_fixed_JVDB_y-compact.png)
*Figure 1: Vision Series: three-step verification rail*

### 5.1 Stage 1: Component testing
- **Focus**: IC products are tested in test sockets across multiple conditions as specified in their individual test plans. These production tests focus on maximizing test coverage to ensure the early detection of any manufacturing defects. 
- **Products**: MAG-IMG002x1-NC, MAG-PSU00001-NP, MAG-CXP00002-NP.
- **Description**: This stage covers Trimming and Final Test (FT) of the individual integrated circuits. Testing procedures include continuity checks, I/O pin tests, interface tests, and parametric testing (including optional trimming). Functional verification and application-specific testing are also performed in addition to tests specific for the product family.

### 5.2 Stage 2: Populated PCBs
- **Focus**: Functional verification of assembled PCB products
- **Products**: MAG-VIS4000x-N (Imaging PCB), MAG-VIS4001x-N (Power PCB), MAG-VIS4003x-N (Serializer PCB).
- **Description**: This stage covers the functional testing of post-assembly boards prior to stack integration. Verifies that the soldering and board-level interconnects are reliable and that the individual sub-systems function correctly.

### 5.3 Stage 3: Integrated module
- **Focus**: Verification of the fully integrated module
- **Products**: MAG-VIS100xx-N (Three-PCB vertical stack).
- **Description**: This stage covers the Module Final Test (MFT). It verifies the CoaXPress downlink/uplink and power delivery across the entire module scope. This final stage validates high-speed timing and synchronization between the different components, ensuring any timing errors are caught at full operational speed.

---

## 6. Test specifications

While the previous chapter outlined the high-level verification progression of the Vision Series products along the horizontal process rail, this chapter provides the detailed test specifications for each product, organized by verification stage.

### 6.1 Stage 1: IC Test Specifications

This section covers the production and trimming tests for the individual integrated circuits. ICs are tested in test sockets across multiple conditions, focusing on maximizing test coverage for early detection of manufacturing defects.

#### 6.1.1 MAG-IMG002x1-NC (Image Sensor IC)

##### Test flow

The production and trimming test flows for the image sensor are depicted below. The production flow covers electrical verification, visual inspection, and optical testing. A separate trim flow is used to calibrate internal references and timing settings.

![MAG-IMG002x1-NC Production Test Flow](vision-module-testing-diagrams/IMG002x1_production_test_flow.png)
*Figure 2: MAG-IMG002x1-NC Production Test Flow*

![MAG-IMG002x1-NC Trim Test Flow](vision-module-testing-diagrams/IMG002x1_trim_test_flow.png)
*Figure 3: MAG-IMG002x1-NC Trim Test Flow*

*Production test stages:*
- **FT (Final Test):** Confirms that the product is compliant against test limits. This stage performs full electrical parametric verification of the image sensor, including continuity, power supply integrity, I/O thresholds, output drive strength, and power consumption measurements.
- **VI (Visual Inspection):** Examination of external surfaces, glass lid, and wire bonding. This inspection identifies visible defects such as cracks, delamination, contamination, or bond wire anomalies before the device proceeds to optical testing.
- **OT (Optical Test):** Characterization of the optical performance of the image sensor. This stage validates dynamic range, pixel response uniformity, dark current, and other electro-optical parameters.

*Trim test stages:*
- **TRIM @ RT:** Trimming at room temperature. Internal references are calibrated to their target values by applying and verifying trim codes at room temperature.
- **Compute best-fit trim values:** Post-processing of measured trim data to compute best-fit trim values for wafer or wafer lot and generate DCF file per mode.

##### Test procedures
- **Continuity:** Verifies that there are no open or short circuits on the pins.
- **Power Short:** Checks for shorts between power supplies and ground.
- **Leakage:** Measures the input leakage current on control pins.
- **VIL/VIH:** Measures the input low and high voltage thresholds.
- **VOL/VOH:** Measures the output low and high voltage levels.
- **IOL/IOH:** Measures the output drive strength.
- **IDDD:** Measures the digital and analog power consumption.
- **Trim test:** Trims internal references to target values.

#### 6.1.2 MAG-CXP00002-NP (CXP Interface IC)

##### Test flow

The production test flow for the serializer IC is depicted below. After device assembly, the chip undergoes trimming and OTP programming, followed by a comprehensive final test.

![MAG-CXP00002-NP Production Test Flow](vision-module-testing-diagrams/CXP00002_production_test_flow.png)
*Figure 4: MAG-CXP00002-NP Production Test Flow*

*Production test stages:*
- **TRIM @ RT, Vnom + write OTP:** Trimming at room temperature and nominal voltage. Internal references and biasing are calibrated, and one-time programmable memory is written with the final trim configuration.
- **FT (Final Test):** Confirms functional and parametric compliance of the serializer. Verifies electrical parameters against specification limits after trimming to ensure the device operates within its intended performance envelope.

##### Test procedures
- **Continuity / Power Short:** Verifies no open/short circuits on pins and supplies.
- **Leakage:** Measures input leakage current.
- **Functional Test:** Validates video transmission, SPI communication, and CXP link stability.

#### 6.1.3 MAG-PSU00001-NP (Power Management IC)

##### Test flow

The production test flow for the DC/DC converter IC is depicted below. The IC undergoes connectivity and parametric testing after assembly.

![MAG-PSU00001-NP Production Test Flow](vision-module-testing-diagrams/PSU00001_production_test_flow.png)
*Figure 5: MAG-PSU00001-NP Production Test Flow*

*Production test stages:*
- **CONN (Connectivity Test):** Checks for shorts on the DUT interface. DUTs must pass this stage before proceeding to ensure the test socket contact is reliable and no assembly defects are present.
- **FT (Final Test):** Verifies the chip is within specifications. Checks all electrical parameters (voltage levels, thresholds, regulation, efficiency) against defined minimum and maximum spec limits.

##### Test procedures
- **Power Short:** Verifies no shorts on input/output power pins.
- **Load Short:** Verifies the converter's response to a shorted load.
- **Leakage:** Measures input leakage current on control pins.
- **Input Threshold:** Measures VIL/VIH voltage thresholds on digital inputs.
- **Output Drive-Strength:** Measures the output drive capability of digital outputs.
- **On-chip Regulator:** Verifies the internal voltage regulator performance.
- **Under Voltage Lock Out (UVLO):** Verifies the UVLO thresholds to ensure the converter shuts down safely at low input voltages.
- **Output Voltage Monitor:** Validates the power-good output monitoring functionality.
- **Over Temperature Protection:** Verifies the thermal shutdown mechanism.
- **Startup Behaviour:** Characterizes the power-up ramp and timing.
- **Line Regulation:** Measures output voltage stability over the input voltage range.
- **Load Regulation:** Measures output voltage stability over the load current range.
- **Efficiency:** Measures the converter's power conversion efficiency under various loads.

### 6.2 Stage 2: Populated PCB Test Specifications

This section covers the functional testing of the three post-assembly sub-boards (Imaging, Serializer, and Power PCBs) prior to stack integration. Each PCB is populated with pre-tested IC components from Stage 1. All three boards share a common test philosophy: an initial "Approved device" input gate verifies that only pre-tested Stage 1 components are used, followed by board-level assembly and a Vision (VIS) functional test that validates the sub-system operates correctly at the PCB level.

#### 6.2.1 Test flows

The production test flows for the three populated PCBs are depicted below. While the overall structure is similar across all boards, the specific test content differs to match each sub-system's functionality.

**MAG-VIS4000x-N (Imaging PCB)** -- Pre-tested image sensor components from Stage 1 are assembled onto the PCB, followed by a functional test of the board-level imaging chain.

![MAG-VIS4000x-N Production Test Flow](vision-module-testing-diagrams/VIS4000x_production_test_flow.png)
*Figure 6: MAG-VIS4000x-N Production Test Flow*

**MAG-VIS4003x-N (Serializer PCB)** -- Pre-tested serializer and DC/DC converter components from Stage 1 are assembled onto the PCB, followed by a functional test of the CXP link and power delivery sub-system.

![MAG-VIS4003x-N Production Test Flow](vision-module-testing-diagrams/VIS4003x_production_test_flow.png)
*Figure 7: MAG-VIS4003x-N Production Test Flow*

**MAG-VIS4001x-N (Power PCB)** -- Pre-tested DC/DC converter components from Stage 1 are assembled onto the board, followed by connectivity checking and a functional test of voltage regulation and ripple performance. This board additionally includes a CONN (Connectivity Test) stage before the VIS test.

![MAG-VIS4001x-N Production Test Flow](vision-module-testing-diagrams/VIS4001x_production_test_flow.png)
*Figure 8: MAG-VIS4001x-N Production Test Flow*

#### 6.2.2 Test stages

All three PCBs share the **VIS (Vision Test)** stage as their primary functional verification. The Power PCB additionally includes a **CONN** stage. The specific scope of each VIS test is:

- **VIS4000x -- VIS (Vision Test):** Functional test of the assembled imaging PCB. Validates that the board-level interconnects and the image sensor readout chain operate correctly after PCB population.
- **VIS4003x -- VIS (Vision Test):** Functional test of the assembled serializer PCB. Validates the CXP link functionality and power delivery sub-system at the board level.
- **VIS4001x -- CONN (Connectivity Test):** Checks for shorts on the DUT interface at the board level, verifying that PCB assembly and soldering have not introduced connection faults.
- **VIS4001x -- VIS (Vision Sub-board Test):** Verifies functionality of the DCDC sub-board on the MAG-VIS400xx PCBs, including voltage-level accuracy and ripple under the expected load-profile.

#### 6.2.3 Test procedures

*MAG-VIS4000x-N and MAG-VIS4003x-N:*
- **Functional Test:** Validates the assembled PCB functionality, including power delivery, signal integrity, and sub-system communication (image sensor readout for VIS4000x; CXP link and power delivery for VIS4003x).

*MAG-VIS4001x-N:*
- **Power Short:** Verifies no shorts on input/output power pins.
- **Load Short:** Verifies the converter's response to a shorted load.
- **Leakage:** Measures input leakage current on control pins.
- **Input Threshold:** Measures VIL/VIH voltage thresholds on digital inputs.
- **Output Drive-Strength:** Measures the output drive capability of digital outputs.
- **On-chip Regulator:** Verifies the internal voltage regulator performance.
- **Under Voltage Lock Out (UVLO):** Verifies the UVLO thresholds to ensure the converter shuts down safely at low input voltages.
- **Output Voltage Monitor:** Validates the power-good output monitoring functionality.
- **Over Temperature Protection:** Verifies the thermal shutdown mechanism.
- **Startup Behaviour:** Characterizes the power-up ramp and timing.
- **Line Regulation:** Measures output voltage stability over the input voltage range.
- **Load Regulation:** Measures output voltage stability over the load current range.
- **Efficiency:** Measures the converter's power conversion efficiency under various loads.

### 6.3 Stage 3: Integrated Module Test Specifications

This section covers the Module Final Test (MFT) for the fully integrated vision module. It verifies the CoaXPress downlink/uplink and power delivery across the entire module scope, validating high-speed timing and synchronization between the different components.

#### 6.3.1 MAG-VIS100xx-N (Three-PCB Vertical Stack)

##### Test flow

The production test flow for the fully integrated vision module is depicted below. Pre-tested and approved PCBs from Stage 2 (Imaging, Power, and Serializer boards) are assembled into the final three-PCB vertical stack, followed by visual inspection and comprehensive functional verification.

![MAG-VIS100xx-N Production Test Flow](vision-module-testing-diagrams/VIS100xx_production_test_flow.png)
*Figure 9: MAG-VIS100xx-N Production Test Flow*

*Production test stages:*
- **VI (Visual Inspection):** Assessment of the physical condition of the assembled module to identify visible defects before electrical testing. Checks for cracks, pin issues, delamination, solder anomalies, or mechanical damage on the integrated stack.
- **VER (Functional Verification):** Confirms that the integrated module is compliant (functional and parametric) against its specifications for normal use-cases. This stage validates CXP downlink/uplink communication, power delivery across the module, image data integrity, and trigger functionality at full operational speed.

##### Test procedures
- **Visual Inspection:** Assessment of physical condition, identification of cracks, pin issues, delamination, or mechanical damage.
- **Power Consumption:** Measures the total power consumption of the module at the system level.
- **CXP Core Functionality and Video Data Check:** Validates the CoaXPress downlink (1.25 Gbps) and uplink (20 Mbps) communication and verifies image data integrity.
- **IMG Core Functionality and Video Data Check:** Verifies the image sensor readout through the serializer, confirming correct pixel data and frame rates.
- **IMG Trigger Mode:** Validates the external trigger functionality of the image sensor for synchronized acquisition.

---

## 7. Product Specifications & Acceptance Criteria

The key specifications for the Vision Series products are extracted from their respective datasheets. The acceptance criteria and test limits are defined in the production test plans.

### 7.1 MAG-IMG002X1-NC (Full HD CMOS Image Sensor)

**Table 1: MAG-IMG002X1-NC Key Specifications**

| Parameter | Specification | Test Condition / Acceptance Criteria |
| :--- | :--- | :--- |
| **Resolution** | 1920 x 1080 (Full HD) | Validated via image capture test |
| **Frame Rate** | Up to 30 FPS | Validated via continuous mode test |
| **Dynamic Range** | > 60 dB | Characterized during optical test |
| **Supply Voltage** | 1.8V (Digital), 3.3V (Analog) | VDD pin voltage test |
| **Power Consumption** | < 1W (typical) | IDD current measurement |
| **Radiation Hardness (TID)** | > 1 MGy | Guaranteed by design and lot acceptance |
| **Radiation Hardness (SEE)** | > 62.5 MeV.cm²/mg | Guaranteed by design |

### 7.2 MAG-CXP00002-NP (CoaXPress Serializer ASIC)

**Table 2: MAG-CXP00002-NP Key Specifications**

| Parameter | Specification | Test Condition / Acceptance Criteria |
| :--- | :--- | :--- |
| **Downlink Speed** | 1.25 Gbps | Tested via functional interface test |
| **Uplink Speed** | 20 Mbps | Tested via functional interface test |
| **Supply Voltage** | 3.3V | VDD pin voltage test (LSL: 3.0V, USL: 3.6V) |
| **Power Consumption** | 272 mW (typical) | IDD current measurement |
| **Clock Input** | 10 - 40 MHz | Tested via PLL lock verification |
| **Radiation Hardness (TID)** | > 1 MGy (100 Mrad) | Guaranteed by design and lot acceptance |
| **Radiation Hardness (SEE)** | > 60 MeV.cm²/mg | Guaranteed by design |

### 7.3 MAG-PSU00001-NP (10W Synchronous Step-Down DC/DC Converter)

**Table 3: MAG-PSU00001-NP Key Specifications**

| Parameter | Specification | Test Condition / Acceptance Criteria |
| :--- | :--- | :--- |
| **Input Voltage Range** | 5V to 11V | UVLO High (LSL: 4.4V, USL: 4.8V) |
| **Load Capability** | 4A (active cooling) | IOL/IOH current tests |
| **Switching Frequency** | 1 - 3 MHz | Functional switching test |
| **Input Leakage Current** | - | LSL: -10mA, USL: 10mA |
| **VIL (Input Low Voltage)** | 0.73V (typical) | LSL: 0.67V, USL: 0.78V |
| **VIH (Input High Voltage)** | 0.815V (typical) | LSL: 0.77V, USL: 0.90V |
| **Radiation Hardness (TID)** | > 1 MGy | Guaranteed by design and lot acceptance |
| **Radiation Hardness (SEE)** | 64 MeV.cm²/mg | Tested free of destructive SEEs |

### 7.4 MAG-VIS100xx-N (Electronic Vision Module)

**Table 4: MAG-VIS100xx-N Key Specifications**

| Parameter | Specification |
| :--- | :--- |
| **Components** | MAG-IMG002X1, MAG-CXP0002, 2x MAG-PSU00001 |
| **Input Voltage** | 9V (generates 3.3V and 1.8V internally) |
| **Video Interface** | CoaXPress 1.25 Gbps (75-Ohm coax) |
| **Radiation Hardness** | > 1 MGy TID (Si) |
| **Operating Temp** | 0 to 50 °C ambient |
