## Revision History

| Revision | Date | Description | Author |
| :--- | :--- | :--- | :--- |
| 1.0 | 2026-04-10 | Initial draft of the Vision Series Test Plan | Jonathan Vanden Berk |
| 1.1 | 2026-04-13 | Updated diagrams and test stage descriptions | Jonathan Vanden Berk |
| 1.2 | 2026-04-15 | Added product specifications and acceptance criteria | Jonathan Vanden Berk |
| 1.3 | 2026-04-22 | Tightened USLs for MAG-IMG002x1-NC bad-row/bad-column (T0035) and PRNU global outliers (T0038), and added PROD/EM/reject bin classification to the pixel-array defect and hot-pixel/DSNU/PRNU outlier parameter descriptions | Jonathan Vanden Berk |

## Introduction & Scope

This document outlines the verification framework for Magics Technologies’ Vision Series products to ensure all quality targets are met. The Vision Series encompasses a diverse range of hardware, including standalone radiation-hardened ICs (Image Sensor (MAG-IMG002x1-NC), Serializer (MAG-CXP00002-NP), and DC/DC Converter (MAG-PSU00001-NP)) and fully integrated electronic Vision Modules (MAG-VIS100xx-N).

This test plan details the test flows, conditions, and stages, alongside the production and trimming procedures required to guarantee the reliability and performance of each product. Furthermore, this document defines the direct relationship between datasheet specifications and the specific test parameters used to verify them.

This document specifically covers the production screening and verification procedures performed on every manufactured unit to guarantee zero-hour quality and compliance with datasheet specifications. 

Long-term reliability (e.g., High-Temperature Operating Life, thermal cycling, mechanical shock) and radiation tolerance (TID, SEE) are guaranteed by design and verified through separate periodic qualification campaigns. These are documented in dedicated product qualification reports and are outside the scope of this production test plan.

---

## Vision products verification process

The verification and testing of the Vision Series products follow a three-step horizontal process rail. This ensures that quality is maintained incrementally from the IC component level up to the fully integrated module. While testing a MAG-VIS100xx product spans from component to module, our verification is gated: customers purchasing IC-only or PCB products receive components that have successfully cleared the specific segments of the rail required for those tiers.

![Vision Series: three-step verification rail](vision-module-testing-diagrams/diagram-1-option-c-process-rail_fixed_JVDB_y-compact.png)
*Figure 1: Vision Series: three-step verification rail*

### Level 1: Component verification
- **Focus**: IC products are tested in test sockets across test conditions as specified in their individual test plans. These production tests focus on maximizing test coverage to ensure the early detection of any manufacturing defects. 
- **Products**: MAG-IMG002x1-NC, MAG-PSU00001-NP, MAG-CXP00002-NP.
- **Description**: This level covers Trimming and Final Test (FT) of the individual integrated circuits. Electro-optical and image sensor array defect testing is included for the MAG-IMG002x1-NC. Testing procedures include continuity checks, I/O pin tests, interface tests, and parametric testing (including optional trimming). Functional verification and application-specific testing are also performed in addition to tests specific for the product family.

### Level 2: PCB verification
- **Focus**: Functional verification of assembled PCB products
- **Products**: MAG-VIS4000x-N (Imager PCB), MAG-VIS4001x-N (Power PCB), MAG-VIS4003x-N (Serializer PCB).
- **Description**: This level covers the functional testing of post-assembly boards prior to stack integration. Verifies that the soldering and board-level interconnects are reliable and that the individual sub-systems function correctly.

### Level 3: Module verification
- **Focus**: Verification of the fully integrated module
- **Products**: MAG-VIS100xx-N (Three-PCB vertical stack).
- **Description**: This level covers the Module Final Test (MFT). It verifies the CoaXPress downlink/uplink and power delivery across the entire module scope. This final product level test validates high-speed timing and synchronization between the different components, ensuring any timing errors are caught at full operational speed.

---

## Test specifications

While the previous chapter outlined the high-level verification of the Vision Series products along the horizontal process rail, this chapter provides the detailed test specifications for each product, organized by product level test.

Note that the test procedures listed in this chapter measure significantly more parameters than those published in the product datasheets. The additional data collection serves Magics internal process monitoring: it enables detailed analysis of block and function-level performance on each IC, tracking of parametric drift over production lots, and early detection of process shifts. All internal parameters have defined limits and are actively monitored during production. To keep this report concise, only the parameters that are specified in the product datasheets are discussed in the acceptance criteria of Chapter 5.

### Level 1: IC Test Specifications

This section covers the production and trimming tests for the individual integrated circuits. ICs are tested in test sockets across multiple conditions, focusing on maximizing test coverage for early detection of manufacturing defects.

#### MAG-IMG002x1-NC (Image Sensor IC)

##### Test flow

The production and trimming test flows for the image sensor are depicted below. The production flow covers electrical verification, visual inspection, and optical testing. A separate trim flow is used to calibrate internal references and timing settings. This trim flow is performed on a subset of each wafer batch, from this subset the best fit values for the batch are calculated and the DCF files are generated. 

![MAG-IMG002x1-NC Production Test Flow](vision-module-testing-diagrams/IMG002x1_production_test_flow.png)
*Figure 2: MAG-IMG002x1-NC Production Test Flow*

![MAG-IMG002x1-NC Trim Test Flow](vision-module-testing-diagrams/IMG002x1_trim_test_flow.png)
*Figure 3: MAG-IMG002x1-NC Trim Test Flow*

##### Test conditions

The tables below define the temperature and supply voltage test conditions used across the IMG002x1 electrical and electro-optical test stages. Each test stage references a subset of these conditions (Min, Nom, and/or Max). The different supply domains are coupled, meaning that, for example, if the Max supply condition is chosen for a certain test stage, all supply domains will be set to their Max values. Cross-corners settings such as Analog at Vnom and Digital at Vmax are not allowed.

*Table: MAG-IMG002x1-NC Temperature Conditions*

| Condition | Symbol | Min | Nom | Max | Unit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Temperature | Temp | 0 (CT) | 25 (RT) | 85 (HT) | °C |

*Table: MAG-IMG002x1-NC Supply Voltage Conditions*

| Condition | Symbol | Min | Nom | Max | Unit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Digital supply voltage | VDDD | 1.62 | 1.8 | 1.98 | V |
| Analog supply voltage | VDDA | 3.135 | 3.3 | 3.63 | V |
| IO supply voltage | VDDIO | 3.135 | 3.3 | 3.63 | V |
| Pixel reset voltage | VD_RST | 3.135 | 3.3 | 3.63 | V |

In the test stage section below, the default test conditions for each stage are listed. Sometimes there is a need to include or exclude specific conditions for a particular test procedure, this will be noted in the test procedure section. If the Conditions field is empty, the default test conditions apply.

##### Test stages
*Production test stages:*
- **FT (Final Test):** Confirms that the product is compliant against test limits. This stage performs full electrical parametric verification of the image sensor, including continuity, power supply integrity, I/O thresholds, output drive strength, and power consumption measurements. Test conditions are: CT/RT/HT and Vmin/Vnom/Vmax, FHD10 mode, dark current related parameters are calculated from a ROI of 400 x 400 pixels in the center of the array. The sensor array is covered from any light input.
- **VI (Visual Inspection):** Examination of external surfaces, glass lid, and wire bonding. This inspection identifies visible defects such as cracks, delamination, contamination, or bond wire anomalies before the device proceeds to optical testing.
- **OT (Optical Test):** Verification of the optical performance of the image sensor. This stage validates dynamic range, pixel response uniformity, dark current, and other electro-optical parameters. The pixel array is also tested for defects in pixels, rows, and columns. Test conditions are: RT (ambient) and Vnom, FHD10 mode, dark current related parameters are calculated from a ROI of 400 x 400 pixels in the center of the array.

*Trim test stages:*
- **TRIM @ RT:** Trimming at room temperature. Internal references are calibrated to their target values by applying and verifying trim codes at room temperature. Test conditions are: RT and Vnom.
- **Compute best-fit trim values:** Post-processing of measured trim data to compute best-fit trim values per wafer or wafer lot and generate a DCF file per mode.

##### Test procedures

The table below lists all test procedures applicable to the MAG-IMG002x1-NC and indicates in which test stage each procedure is executed. The FT stage provides full electrical parametric coverage, while TRIM focuses on calibrating internal references. The OT stage validates optical performance under controlled illumination. The Conditions column notes any deviation from the default test conditions for that test stage, an empty cell means the default conditions listed under Test stages section applies.

*Table: MAG-IMG002x1-NC Test Procedures*

| Test procedure | Description | Conditions | FT | TRIM | OT |
| :--- | :--- | :--- | :---: | :---: | :---: |
| Continuity | Each pin is connected to an SMU with power supplies off. A small current is forced into the pin, and the resulting voltage drop over the ESD structure is measured to verify proper pin connectivity. | | X | X | X |
| Power Short | Checks for shorts on the power rails by supplying a very low voltage and measuring the resulting current per power domain. | | X | X | X |
| Leakage | Measures the leakage current of each input pin or tristate output pin. | | X | X | |
| VIL/VIH | Checks the input hysteresis of all digital input pins by sweeping the input voltage and observing the digital state transition. | | X | | |
| VOL/VOH | Measures the low and high voltage of digital outputs at 1 mA load. | | X | | |
| IOL/IOH | Measures the low and high level output current of digital outputs. | | X | | |
| IDDD | Measures the current consumption of the DUT in multiple states, video modes, frame rates and test patterns. | FHD10/HD40/VGA50 | X | X | |
| Test buffer offset | Measures the offset of both test buffers on the test mux. | | X | X | |
| Static signal test | Measures the voltage/current of certain internal signals. | | X | | |
| PLL open-loop | Measures the open-loop frequency of the VCO while forcing the VCO voltage. | | X | | |
| PLL lock | Checks the lock status and measures the PLL-lock frequency. | | X | | |
| Ramp gen test | Measures the delay of the readout circuitry. | | X | | |
| POR | Validates the power-on reset behaviour of the device. | | X | | |
| Trigger mode | Generates an external trigger pulse and validates the DUT responds correctly. | | X | | |
| Testpattern generator | Tests the internal testpattern generator by comparing a captured image with a predefined reference. | | X | | |
| Serial interface | Validates the SPI serial interface functionality. | | X | X | X |
| Trim test | Trims each internal block (voltage reference, current reference) by sweeping trim codes and selecting the best-fit value. | | | X | |
| Ramp gen trim | Trims the ramp generator circuitry to target voltage and slope values. | | | X | |
| Frame modes | Validates the different video modes by capturing and verifying images. | FHD10/HD40/VGA50 | | | X |
| Blackpixel readout | Tests the black reference pixel readout. | | | | X |
| Optical init | Defines the exposure time range required for correct linear fitting in DC and PTC analysis, and measures light nonuniformity. | | | | X |
| Optical defect map | Captures raw images to map bright/dead pixels, rows and columns. | | | | X |
| Optical PTC capture | Captures raw images necessary for Photon Transfer Curve (PTC) and spatial nonuniformity (SN) analysis. | | | | X |
| Optical DC capture | Captures raw images necessary for dark current (DC) per pixel analysis. | | | | X |
| Optical test processing | Reads raw images from previous tests and performs PTC, SN and DC per pixel analysis. Results are combined and reported to the results database. | | | | X |


The table below maps each test procedure to the datasheet parameters it verifies. Parameters are listed by their Chapter 5 name. Note that only a subset of the test procedures is used to cover all datasheet parameters.

*Table: MAG-IMG002x1-NC Parameter Traceability*

| Test procedure | Test ID | Parameters measured |
| :--- | :--- | :--- |
| VIL/VIH | T0004 | TRIG_IN input threshold low, TRIG_IN input threshold high, TRIG_IN input hysteresis, RSTB input threshold (no hysteresis), SPI input threshold low, SPI input threshold high, SPI input hysteresis |
| VOL/VOH | T0005 | SPI MISO output voltage (no load), VOH (no resistive load), VOL (no resistive load) |
| IDDD | T0007 | VDDD current (active, FHD10 10-bit), VDDA+VDDIO+VD_RST current (active, FHD10 10-bit) |
| Static signal test | T0010 | Bandgap reference voltage (VDD12BG) |
| Frame modes | T0024 | Pixel output clock speed, Data output line speed |
| Optical test processing | T0038 | Conversion gain, Responsivity, Temporal noise, Dynamic range, SNR_MAX, Dark current (DC), Dark current non uniformity (DCNU), Dark signal non uniformity (DSNU), Photo response non uniformity (PRNU) |

#### MAG-CXP00002-NP (CXP Interface IC)

##### Test flow

The production test flow for the serializer IC is depicted below. After device assembly, the chip undergoes trimming and OTP programming, followed by a comprehensive final test (FT). Trimming is done per part. 

![MAG-CXP00002-NP Production Test Flow](vision-module-testing-diagrams/CXP00002_production_test_flow.png)
*Figure 4: MAG-CXP00002-NP Production Test Flow*

##### Test conditions

The tables below define the temperature and supply voltage test conditions used across the CXP00002 test stages. Each test stage references a subset of these conditions (Min, Nom, and/or Max). The CXP00002 has a single 3.3 V supply level that is shared over all the domains (Digital, PLL and Analog).

*Table: MAG-CXP00002-NP Temperature Conditions*

| Condition | Symbol | Min | Nom | Max | Unit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Temperature | Temp | -40 (CT) | 25 (RT) | 85 (HT) | °C |

*Table: MAG-CXP00002-NP Supply Voltage Conditions*

| Condition | Symbol | Min | Nom | Max | Unit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Supply voltage | VDD3V3 | 2.97 | 3.3 | 3.63 | V |

In the test stage section below, the default test conditions for each stage are listed. Sometimes there is a need to include or exclude specific conditions for a particular test procedure, this will be noted in the test procedure section. If the Conditions field is empty, the default test conditions apply.

##### Test stages

*Production test stages:*
- **FT (Final Test):** Confirms functional and parametric compliance of the serializer. Verifies electrical parameters against specification limits after trimming. Test conditions are: CT/RT/HT and Vmin/Vnom/Vmax at the time of writing. Worst-case conditions will be set when sufficient characterization data is acquired.

*Trim test stages:*
- **TRIM @ RT, Vnom + write OTP:** Trimming at room temperature and nominal voltage. Internal references are calibrated, and one-time programmable memory is written with the final trim configuration. Test conditions are: RT and Vnom.

##### Test procedures

The table below lists all test procedures applicable to the MAG-CXP00002-NP and indicates in which test stage each procedure is executed. The TRIM stage calibrates internal LDOs and references and programs the OTP memory, after which the FT stage verifies the full parametric and functional performance of the serializer, including its high-speed CXP interface and SPI communication channels. The Conditions column notes any deviation from the default test conditions for that test stage, an empty cell means the default conditions listed under Test stages section applies.

*Table: MAG-CXP00002-NP Test Procedures*

| Test procedure | Description | Conditions | FT | TRIM |
| :--- | :--- | :--- | :---: | :---: |
| Continuity | Each pin is connected to an SMU with power supplies off. A small current is pushed into the pin to verify proper pin connectivity via the ESD diode voltage drop. | | X | X |
| Power Short | Checks for shorts on the power rails by supplying a very low voltage and measuring the resulting current per power domain. | | X | X |
| Pin leakage | Measures the leakage current of each input pin or tristate output pin by applying low and high voltage and measuring the current. | | X | X |
| VIL/VIH | Checks the input hysteresis of all digital input pins by performing high-to-low and low-to-high voltage sweeps. | | X | |
| VOH/VOL | Measures the low and high voltage of digital outputs under a load current of 1 mA. | | X | |
| IOL/IOH | Measures the low and high level output current of digital outputs. | | X | |
| IDDD | Measures the current consumption of the DUT in multiple states, video modes, frame rates. | FHD/HD/VGA, 10fps/25fps | X | X |
| Test Buffer Offset | Measures the offset of both test buffers on the test mux by creating a loop through GPIO pins and sweeping the input voltage. | | X | X |
| Static Signal Test | Measures all static signals available on the test mux and stores results in the database. | | X | |
| Regulators | Performs a load test on the LDOs with external decoupling by sweeping load currents and measuring the internal output voltage through the test mux. | Vmin/Vmax | X | |
| Oscillator | Checks the reference clock circuits of the DUT. | | X | |
| PLL Open Loop | Checks the PLL open loop behaviour by opening the loop and measuring the v_tune voltage range. | | X | |
| PLL Lock | Checks the PLL closed loop behaviour by observing key parameters of the locked PLL. | | X | |
| IO SPI Slave | Validates the debug SPI slave interface by reading and writing registers. | | X | X |
| IO SPI Master CAM | Validates the camera SPI master interface by reading and writing a register in the FPGA acting as SPI slave. | | X | |
| IO SPI Master GPIO | Validates the GPIO SPI master interface by reading and writing a register in the FPGA acting as generic SPI slave. | | X | |
| CXP Uplink Receiver Sensitivity | Checks receiver sensitivity using a function generator to send CXP sequences at varying amplitudes, performing a binary search for the sensitivity threshold. | | X | |
| Internal Test Patterns | Validates the internal test pattern generator by looping over test patterns and capturing them with the frame grabber. | FHD/HD/VGA, 8b/10b/12b, 13 test patterns | X | |
| Camera Test | Sends and captures test patterns from an external camera (FPGA pattern generator) and compares raw pixel values with a reference. | FHD/HD/VGA, 8b/10b/12b | X | |
| OTP Data Retention | Reads data from OTP and verifies that no bits are flipped. | | X | X |
| Block Trimming | Trims each block (LDO, voltage reference, current reference) by performing a sweep and selecting the trim setting closest to the target value. | | | X |
| OTP Write | Writes the final trim configuration data into the OTP cells and verifies successful programming. | | | X |


The table below maps each test procedure to the datasheet parameters it verifies. Parameters are listed by their Chapter 5 name. Note that only a subset of the test procedures is used to cover all datasheet parameters.

*Table: MAG-CXP00002-NP Parameter Traceability*

| Test procedure | Test ID | Parameters measured |
| :--- | :--- | :--- |
| VIL/VIH | T0004 | VIL (GPIO input low threshold), VIH (GPIO input high threshold), Hysteresis (GPIO), VIL (Video input low threshold), VIH (Video input high threshold), Hysteresis (Video) |
| IDDD | T0007 | 3.3V total supply current (average), 3.3V digital supply current (average), 3.3V analog supply current (average), 3.3V PLL supply current (average), Total power consumption |
| Regulators | T0011 | VDD1V2_CAM reference voltage |
| Regulators | T0012 | VDD1V8_CAM supply voltage |
| Oscillator | T0013 | Crystal frequency |
| Camera Test | T0023 | Parallel video data rate |

#### MAG-PSU00001-NP (Power Management IC)

##### Test flow

The production test flow for the DC/DC converter IC is depicted below. The IC undergoes connectivity (CONN) and final test (FT) after device assembly.

![MAG-PSU00001-NP Production Test Flow](vision-module-testing-diagrams/PSU00001_production_test_flow.png)
*Figure 5: MAG-PSU00001-NP Production Test Flow*

##### Test conditions

The tables below define the temperature and input voltage test conditions used across the PSU00001 test stages. Each test stage references a subset of these conditions (Min, Nom, and/or Max). The PSU00001 is a DC/DC converter with a single input voltage domain.

*Table: MAG-PSU00001-NP Temperature Conditions*

| Condition | Symbol | Min | Nom | Max | Unit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Temperature | Temp | -40 (CT) | 25 (RT) | 85 (HT) | °C |

*Table: MAG-PSU00001-NP Input Voltage Conditions*

| Condition | Symbol | Min | Nom | Max | Unit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Input voltage | Vin | 5 | 9 | 11 | V |

In the test stage section below, the default test conditions for each stage are listed. Sometimes there is a need to include or exclude specific conditions for a particular test procedure; this will be noted in the test procedure section. If the Conditions field is empty, the default test conditions apply.

##### Test stages

*Production test stages:*
- **CONN (Connectivity Test):** Checks for shorts on the DUT interface. DUTs must pass this stage before proceeding to ensure the test socket contact is reliable and no assembly defects are present. Test conditions are: RT and Vnom.
- **FT (Final Test):** Verifies the chip is within specifications. Checks all electrical parameters (voltage levels, thresholds, regulation, efficiency) against defined minimum and maximum spec limits. Test conditions are: CT/RT/HT and Vmin/Vnom/Vmax at the time of writing. Worst-case conditions will be set when sufficient characterization data is acquired.

##### Test procedures

The table below lists all test procedures applicable to the MAG-PSU00001-NP. The PSU00001 does not include trimming or NVM programming. The CONN connectivity check is performed as a gate before the FT procedures listed here. The Conditions column notes any deviation from the default test conditions for that test stage, an empty cell means the default conditions listed under Test stages section applies.

*Table: MAG-PSU00001-NP Test Procedures*

| Test procedure | Description | Conditions | CONN | FT |
| :--- | :--- | :--- | :---: | :---: |
| Power Short | Verifies that there is no short to ground on the power terminals of the chip. | | X | |
| Load Short | Verifies that there is no short to ground or power on the load terminals of the chip. | | X | |
| Leakage | Measures the input leakage current of all accessible input pins. | | | X |
| Input threshold | Finds both the high and low threshold voltages (VIL/VIH) for the Enable pin. | | | X |
| Output drive-strength | Measures the current that can be sunk by the power-good output. | | | X |
| On-chip regulator | Measures the regulator voltage and performs a load regulation test on the internal regulator. | | | X |
| Under Voltage Lock Out | Finds the threshold voltages where the chip enters and exits UVLO. | | | X |
| Output voltage monitor | Checks the +/-6.5% output voltage limits of the control loop by forcing the internal sense voltage. | | | X |
| Over Temperature Protection | Checks the over-temperature protection via the power-good flag and PTAT voltage. In FT test stage only the PTAT voltage is monitored. | | | X |
| Startup behaviour | Measures the start-up behaviour of the output voltage and checks the level/time where the power-good flag goes high. | Rload: 10Ω/50Ω/270Ω | | X |
| Inv_Enable functionality | Checks that the functionality of the Enable pin can be inverted using the Inv_Enable configuration. | | | X |
| Line regulation | Measures the input voltage dependency of the output voltage. | Vout:0.9V/1.2V/1.5V/1.8V/2.0V/2.5V/3.3V, Vmin/Vmax | | X |
| Load regulation | Measures the load current dependency of the output voltage. | Vout:0.9V/1.2V/1.5V/1.8V/2.0V/2.5V/3.3V, Vmin/Vmax, Iload: 0.1A/0.3A/0.5A/0.7A/0.9A/1.1A | | X |
| Efficiency | Measures efficiency over different loads and input/output voltage conditions. | Vout:0.9V/1.2V/1.5V/1.8V/2.0V/2.5V/3.3V, Vmin/Vmax, Iload: 0.5A/0.8A/1.0A, Halfsw:ON/OFF| | X |


The table below maps each test procedure to the datasheet parameters it verifies. Parameters are listed by their Chapter 5 name. Note that only a subset of the test procedures is used to cover all datasheet parameters.

*Table: MAG-PSU00001-NP Parameter Traceability*

| Test procedure | Test ID | Parameters measured |
| :--- | :--- | :--- |
| Input threshold | T0006 | Enable start threshold, Enable stop threshold |
| Under Voltage Lock Out | T0009 | Vin start threshold, Vin stop threshold |
| Output voltage monitor | T0010 | Output Over Voltage PGood threshold, Output Under Voltage PGood threshold |
| Startup behaviour | T0012 | Soft Start duration |

### Level 2: PCB Test Specifications

This section covers the functional testing of the three post-assembly sub-boards (Imager, Serializer, and Power PCBs) prior to stack integration. Each PCB is assembled with one or more pre-tested IC components from level 1. All three boards share a common test philosophy: an initial "Approved device" input gate verifies that only pre-tested level 1 components are used, followed by board-level assembly and a Vision (VIS) functional test stage that validates the sub-system operates correctly at the PCB level. The VIS test stage consists of a collection of test procedures from the component level with optional dedicated tests to increase test coverage.

#### Test flows

The production test flows for the three assembled PCBs are depicted below. While the overall structure is similar across all boards, the specific test content differs to match each sub-system's functionality.

**MAG-VIS4000x-N (Imager PCB)** -- Pre-tested image sensor components from level 1 are assembled onto the PCB, followed by a functional test of the board.

![MAG-VIS4000x-N Production Test Flow](vision-module-testing-diagrams/VIS4000x_production_test_flow.png)
*Figure 6: MAG-VIS4000x-N Production Test Flow*

**MAG-VIS4003x-N (Serializer PCB)** -- Pre-tested serializer and DC/DC converter components from level 1 are assembled onto the PCB, followed by a functional test of the CXP link and power delivery sub-system.

![MAG-VIS4003x-N Production Test Flow](vision-module-testing-diagrams/VIS4003x_production_test_flow.png)
*Figure 7: MAG-VIS4003x-N Production Test Flow*

**MAG-VIS4001x-N (Power PCB)** -- Pre-tested DC/DC converter components from level 1 are assembled onto the board, followed by parametrical test to check voltage load/line regulation behaviour and ripple performance. This board additionally includes a CONN (Connectivity Test) test stage before the VIS test stage.

![MAG-VIS4001x-N Production Test Flow](vision-module-testing-diagrams/VIS4001x_production_test_flow.png)
*Figure 8: MAG-VIS4001x-N Production Test Flow*

#### Test conditions

Since the PCB-level tests are functional verification tests rather than parametric characterisation, all procedures are executed at ambient temperature and nominal supply voltage only. No temperature or supply corner conditions are applied at this level, the underlying IC components have already been fully tested at level 1.

For the MAG-VIS4000x-N (Imager PCB), the image sensor is configured in **FHD10** mode (1920 x 1080 @ 10 fps, 10-bit) during all VIS test procedures.

#### Test stages

All three PCBs share the VIS test stage as their primary functional verification. The Power PCB additionally includes a **CONN** test stage. The specific scope of each VIS test is:

- **VIS4000x -- VIS (Vision Sub-board Test):** Functional test of the assembled imager PCB. Validates that the board-level interconnects and the image sensor readout chain operate correctly after PCB population. The most important verification test in this VIS test stage is the read out of a set of test patterns that are hard coded in the image sensor IC.
- **VIS4003x -- VIS (Vision Sub-board Test):** Functional test of the assembled serializer PCB. Validates the CXP link functionality and power delivery sub-system at the board level. The most important verification test in this VIS test stage is the read-out (via CXP interface) of a set of external test patterns that are applied to the video pins.
- **VIS4001x -- CONN (Connectivity Test):** Checks for shorts and opens at the board level, verifying that PCB assembly and soldering have not introduced connection faults.
- **VIS4001x -- VIS (Vision Sub-board Test):** Verifies functionality of the DCDC sub-board on the MAG-VIS400xx PCBs, including voltage-level accuracy and ripple under worst case DC conditions.

#### Test procedures

The tables below list the test procedures for each PCB during its VIS test stage. These procedures are a subset of the component-level tests, re-used at the board level to verify correct assembly and interconnect integrity. The Power PCB additionally includes a CONN stage for connectivity verification before the VIS tests.

*Table: MAG-VIS4000x-N VIS Test Procedures*

| Test procedure | Description |
| :--- | :--- |
| Testpattern generator | Tests the internal testpattern generator of the image sensor IC via the PCB-level readout chain, comparing the captured image with a predefined reference. |
| Serial interface | Validates SPI communication with the image sensor at the board level. |
| IDD VIS | Measures the power supply current consumption on the VIS board, where supplies with the same voltage level are shorted and sourced as a single channel. |

*Table: MAG-VIS4003x-N VIS Test Procedures*

| Test procedure | Description |
| :--- | :--- |
| IO SPI Master CAM | Validates the camera SPI master interface by reading and writing a register in the FPGA acting as SPI slave. |
| IO SPI Master GPIO | Validates the GPIO SPI master interface by reading and writing a register in the FPGA acting as generic SPI slave. |
| Internal Test Patterns | Validates the internal test pattern generator by looping over test patterns and capturing them with the frame grabber. |
| Camera Test | Sends external test patterns (from FPGA pattern generator) to the video input pins and captures the CXP output to verify pixel-accurate data integrity. |
| OTP Data Retention | Reads data from OTP and verifies that no bits are flipped. |
| VDD3V3 DCDC | Checks the output voltage of the on-board DCDC converter. |

*Table: MAG-VIS4001x-N CONN + VIS Test Procedures*

| Test procedure | Description |
| :--- | :--- |
| Power Short | Verifies that there is no short to ground on the power terminals at the board level. |
| Load Short | Verifies that there is no short to ground or power on the load terminals at the board level. |
| Line regulation | Measures the input voltage dependency of the output voltage at the board level. |
| Load regulation | Measures the load current dependency of the output voltage at the board level. |
| Efficiency | Measures efficiency over different loads and input/output voltage conditions at the board level. |
| Output voltage ripple | Measures ripple amplitude and frequency on the board output. |

### Level 3: Module Test Specifications

This section covers the Module Final Test (MFT) for the fully integrated vision module (MAG-VIS100xx-N, three-PCB vertical stack). It verifies the CoaXPress downlink/uplink and power delivery across the entire module scope, validating high-speed timing and synchronization between the different components.

#### Test flow

The production test flow for the fully integrated vision module is depicted below. Pre-tested and approved PCBs from level 2 (Imager, Power, and Serializer boards) are assembled into the final three-PCB vertical stack, followed by visual inspection and comprehensive functional verification.

![MAG-VIS100xx-N Production Test Flow](vision-module-testing-diagrams/VIS100xx_production_test_flow.png)
*Figure 9: MAG-VIS100xx-N Production Test Flow*

#### Test conditions

The tables below define the temperature, supply voltage, and imager mode test conditions used for the module-level verification. Each test procedure references a subset of these conditions.

*Table: MAG-VIS100xx-N Temperature Conditions*

| Condition | Symbol | Min | Nom | Max | Unit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Temperature | Temp | 0 (CT) | 25 (RT) | 55 (HT) | °C |

*Table: MAG-VIS100xx-N Supply Voltage Conditions*

| Condition | Symbol | Min | Nom | Max | Unit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Module supply voltage | VDD_IN | 6 | 9 | 12 | V |

*Table: MAG-VIS100xx-N Imager Mode Conditions*

| Imager mode | FPS | Image size height | Image size width |
| :--- | :--- | :--- | :--- |
| FHD10 | 10 | 1080 | 1920 |
| FHD30 | 30 | 1080 | 1920 |
| VGA50 | 50 | 480 | 640 |

The default imager mode is FHD10 unless otherwise specified.

#### Test stages

*Production test stages:*
- **VI (Visual Inspection):** Assessment of the physical condition of the assembled module to identify visible defects before electrical testing. Checks for cracks, pin issues, solder anomalies, or mechanical damage on the integrated stack.
- **VER (Functional Verification):** Confirms that the integrated module is compliant (functional and parametric) against its specifications for normal use-cases. This stage validates CXP downlink/uplink communication, power delivery across the module, image data integrity, and trigger functionality at full operational speed. Test conditions are: RT and Vnom.

#### Test procedures

The table below lists all test procedures for the integrated module. The VI stage is a manual inspection performed before any electrical test. The VER stage validates the complete signal chain -- from power delivery through image capture to CXP serialization -- at full operational speed. Module variants that include the MAG-DRV IC have additional driver-specific tests.

*Table: MAG-VIS100xx-N Module Test Procedures*

| Test procedure | Description | VI | VER |
| :--- | :--- | :---: | :---: |
| Visual inspection | Verifies the physical integrity of the assembled module prior to electrical testing, ensuring no mechanical damage, solder defects or contamination is present that could affect performance or safety. | X | |
| Power consumption | Measures the current consumption of the fully integrated module. | | X |
| CXP Core functionality and video data check | Verifies basic functionality of the MAG-CXP00002-NP IC and CoaXPress video data -- checks lock bits, writes and reads a known register via CoaXPress to confirm communication, enables internal test pattern mode and verifies the correct pattern is received by the frame grabber. | | X |
| IMG Core functionality and video data check | Verifies basic functionality of the MAG-IMG002x1 IC -- checks PLL status bits, tests image manipulation logic (y-axis flip), enables the internal Test Pattern Generator (TPG) and verifies the received image pattern via CoaXPress under various video modes and frame rates. | | X |
| IMG Trigger mode | Provides full functional verification of all imager trigger modes: CXP hardware trigger flow, imager free-run burst mode (30-frame burst) and imager software trigger burst mode. | | X |
| MAG-DRV Capabilities (MAG-VIS1001x only) | Verifies functional operation of the MAG-DRV IC outputs in both steady-state (ON/OFF) and dynamic (PWM) modes, using oscilloscope and MUX card to check all channels. | | X |
| MAG-DRV Motor drive capabilities (MAG-VIS1002x only) | Verifies the MAG-DRV IC ability to drive external loads for directional movement of Iris, Zoom and Focus motors, verifying correct drv_enable register values for both directions and safe disable (OFF state). | | X |

---

## Product Specifications & Acceptance Criteria

The key specifications for the Vision Series products are extracted from their respective datasheets and are listed in this chapter. The acceptance criteria and test limits are defined in the production test plans and where extracted from the test system of the product.

### MAG-IMG002x1-NC (Full HD CMOS Image Sensor)

*Table: MAG-IMG002x1-NC Key Specifications*

| Parameter | Datasheet Label | DS Min | DS Typ | DS Max | Unit | LSL | USL | Comment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Current consumption** | | | | | | | | |
| VDDD current (active, FHD10 10-bit) | I_VDDD | - | 205 | 1000 | mA | 20 | 300 | Max 1000 mA only at startup/reset |
| VDDA+VDDIO+VD_RST current (active, FHD10 10-bit) | I_VDDA (combined) | - | 124 | - | mA | 20 | 150 | Split over 3 PSU channels, LSL, USL of VDDA is given here |
| **Clocking and control signal thresholds** | | | | | | | | |
| External clock reference | REFCLK | 10 | 20 | 40 | MHz | - | - | Fixed to 20MHz in test setup Hardware |
| TRIG_IN input threshold low | TRIG_in_l | 0.74 | 1.07 | 1.4 | V | - | - | Pin is of type: rising edge triggered |
| TRIG_IN input threshold high | TRIG_in_h | 1.56 | 1.89 | 2.39 | V | 1.6 | 2.6 | - |
| TRIG_IN input hysteresis | TRIG_in_hyst | 0.66 | 0.82 | 1.15 | V | - | - | Pin is of type: rising edge triggered |
| RSTB input threshold (no hysteresis) | RSTB_th_lvl | - | 1.65 | - | V | 1.4 | 2.3 | - |
| **SPI interface** | | | | | | | | |
| SPI master clock speed | SPI_CLK | - | - | 20 | MHz | - | - | Fixed to 20MHz in test setup Hardware |
| SPI MISO output voltage (no load) | SPI_out | 2.97 | 3.3 | 3.63 | V | 2.7 | - | Tested with 1mA load |
| SPI input threshold low | SPI_in_l | 0.74 | 1.07 | 1.4 | V | 0.6 | 1.7 | s_mosi_vil (representative) |
| SPI input threshold high | SPI_in_h | 1.56 | 1.89 | 2.39 | V | 1.3 | 2.3 | s_mosi_vih (representative) |
| SPI input hysteresis | SPI_in_hyst | 0.66 | 0.82 | 1.15 | V | 0.3 | 0.9 | s_mosi_hysteresis (representative) |
| **Digital video output interface** | | | | | | | | |
| VOH (no resistive load) | VOH | 2.97 | VDDIO | 3.63 | V | 2.7 | - | Tested with 1mA load |
| VOL (no resistive load) | VOL | - | 0 (gnd) | - | V | - | 0.3 | Tested with 1mA load |
| Pixel output clock speed | PIXCLK_speed | 50 | - | 100 | MHz | pass/fail | - | Only tested at speed during characterization (FHD30 mode), production testing uses FHD10, HD40 and VGA50 mode what is at half of the max speed |
| Data output line speed | DV_X_speed | - | - | 50 | MHz | pass/fail | - | Only tested at speed during characterization (FHD30 mode), production testing uses FHD10, HD40 and VGA50 mode what is at half of the max speed |
| **Analog signals** | | | | | | | | |
| Bandgap reference voltage (VDD12BG) | Vvdd12bg | 1.14 | 1.2 | 1.26 | V | 1.05 | 1.35 | - |
| **Electro-optical characteristics** | | | | | | | | |
| Effective number of pixels | - | - | 1920 (H) x 1080 (V) | - | - | - | - | Guaranteed by design |
| Pixel size | - | - | 5um x 5um | - | - | - | - | Guaranteed by design |
| Number of black rows | - | - | 64 | - | - | - | - | Guaranteed by design |
| Shutter type | - | - | Rolling shutter | - | - | - | - | Guaranteed by design |
| Full well charge | - | - | 94000 | - | e- | - | - | This is a design target, related to test parameter: saturation limit. This is tested only during characterization |
| Conversion gain | - | - | 0.01 | - | mV/e- | 0.006 | 0.018 | - |
| Responsivity | - | - | ??? | - | DN/p | 0.02895 | 0.04825 | - |
| Temporal noise | - | - | 66 | - | e- | - | 120 | - |
| Dynamic range | - | - | 62 | - | dB | 57 | 65 | - |
| SNR_MAX | - | - | 49.5 | - | dB | 46 | 54 | - |
| Dark current (DC) | - | - | ??? | - | e-/s/px | - | 2500 | - |
| Dark current non uniformity (DCNU) | - | - | ??? | - | e-/s/px | - | 4000 | - |
| Dark signal non uniformity (DSNU) | - | - | 587.2 | - | e- | - | 600 | - |
| Photo response non uniformity (PRNU) | - | - | < tba | 2.5 | % of mean | -2.5 | 2.5 | - |
| Color filters | - | - | BayerRG (Bayer RGGB) | - | - | - | - | Guaranteed by design |
| Programmable features | - | - | Sensor parameters | - | - | - | - | Features are tested during characterization: Exposure time, sub-sampling, X-Y mirroring, ADC resolution |
| ADC resolution | - | - | 10 and 12 bit | - | - | - | - | Guaranteed by design |
| Interface | - | - | 10/12b parallel output | - | - | - | - | Fixed to 10b for all tests |
| Cover glass lid | Corning 7980 0F | - | - | - | - | - | - | Guaranteed by design |

The table below lists the pixel-array defect test parameters measured during test T0035: Optical defect map. Test limits are continuously refined based on statistical production data to ensure optimal quality and yield.

*Table: MAG-IMG002x1-NC Pixel-Array Defect Test Parameters (T0035)*

| Name | Unit | LSL | USL | Description |
| :--- | :--- | :--- | :--- | :--- |
| Number of dead pixels | px | - | 50 | Dead pixel is a pixel that has unusually low positive or negative response when responding to light (also known as stuck-at pixel or negative gain pixel). Dead pixels from dead rows or columns are excluded from this count. |
| Number of clusters with 2 dead pixels | cl | - | 50 | 2 neigbour dead pixels of same channel |
| Number of clusters with >3 dead pixels | cl | - | 50 | 3 or more neigbour dead pixels of same channel |
| Number of dead rows | rows | - | 5 | Dead row = 100 or more dead pixels in 1 row |
| Number of dead columns | cols | - | 5 | Dead column = 100 or more dead pixels in 1 column |
| Number of bright pixels | px | - | 50 | Bright pixel is a pixel that has unusually high value in dark condition. This can cover pixels with very high outlier values in the pixel DC histogram, or broken pixel/col/row with unusually high offset. Bright pixels from bright rows or columns are excluded from this count. |
| Number of clusters with 2 bright pixels | cl | - | 50 | 2 neigbour bright pixels of same channel |
| Number of clusters with >3 bright pixels | cl | - | 50 | 3 or more neigbour bright pixels of same channel |
| Number of bright rows | rows | - | 5 | Bright row = 100 or more bright pixels in 1 columns |
| Number of bright cols | cols | - | 5 | Bright column = 100 or more bright pixels in 1 columns |
| Number of bad columns | cols | - | 0 | Bad_col = dead_col + bright_col. USL = 0 for production (PROD) parts; parts with 1–5 bad columns are re-binned as engineering model (EM); >5 bad columns → part is rejected. |
| Number of bad rows | rows | - | 0 | Bad_row = dead_row + bright_row. USL = 0 for production (PROD) parts; parts with 1–5 bad rows are re-binned as engineering model (EM); >5 bad rows → part is rejected. |
| Distance between bad columns | cols | 5 | - |  |
| Distance between bad rows | rows | 5 | - |  |

The table below lists the electro-optical and pixel-array defect test parameters measured during test T0038: Optical test processing. Test limits are continuously refined based on statistical production data to ensure optimal quality and yield.

*Table: MAG-IMG002x1-NC Electro-Optical Test Parameters (T0038)*

| Name | Unit | LSL | USL | Description |
| :--- | :--- | :--- | :--- | :--- |
| Typical system gain | DN/e- | 0.022 | 0.066 | System gain = conversion gain / ADC gain (in typ) |
| Dark signal non uniformity (DSNU) local stdev | e- | - | 1500 | Describes offset variation between pixels in close proximity |
| Column FPN without black row correction, global stdev | DN | - | - | Similar to DSNU but without column FPN reduction. In this case, pixel contribution will be much less than column contribution, as expected |
| Column FPN without black row correction, local stdev | DN | - | - |  |
| Number of DSNU global outliers | px | - | 50 | Describes the outliers in the offset histogram. USL = 50 for production (PROD) parts; up to 150 outliers accepted as engineering model (EM); >150 → part is rejected. |
| DSNU global stdev, row contribution | e- | - | 600 |  |
| DSNU global stdev, col contribution | e- | - | 600 | Useful to check if spatial variation is dominated by column or row |
| Number of PRNU global outliers | px | - | 150 | Describes the outliers in the gain histogram. USL = 150 for production (PROD) parts; up to 1000 outliers accepted as engineering model (EM); >1000 → part is rejected. |
| PRNU global stdev, row contribution | % of mean | -2.5 | 2.5 |  |
| PRNU global stdev, col contribution | % of mean | -2.5 | 2.5 | Useful to check if spatial variation is dominated by column or row |
| Hot pixels > criteria 1 | px | - | 1200 | These parameters can represent the tail part of DC histogram. Criteria 1: pixels with value > 5x average of pixels in ROI. USL = 1200 for production (PROD) parts; up to 5000 accepted as engineering model (EM); >5000 → part is rejected. |
| Hot pixels > criteria 2 | px | - | 600 | Criteria 2: pixels with value > 10x average of pixels in ROI. USL = 600 for production (PROD) parts; up to 2500 accepted as engineering model (EM); >2500 → part is rejected. |
| Hot pixels > criteria 3 | px | - | 5 | Criteria 3: pixels with value > 100x average of pixels in ROI. USL = 5 for production (PROD) parts; up to 20 accepted as engineering model (EM); >20 → part is rejected. |
| Percentage of clusters with 2 hot pixels | % | 0 | 100 | cluster size of 2 pixel, because due to crosstalk we expect that hot pixels appear in groups of 2 |
| Percentage of clusters with >3 hot pixels | % | 0 | 100 | to distinguish clusters due to pixel crosstalk or something else |
| Photo response non uniformity (PRNU) local stdev | % of mean | -1 | 1.5 | Describes gain (light response) variation between pixels in close proximity |
| Number of DSNU local outliers | px | - | 50 |  |
| Number of column offset outliers without black correction | col | - | 50 |  |
| Number of PRNU local outliers | px | - | 50 |  |

### MAG-CXP00002-NP (CoaXPress Serializer ASIC)

*Table: MAG-CXP00002-NP Key Specifications*

| Parameter | Datasheet Label | DS Min | DS Typ | DS Max | Unit | LSL | USL | Comment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Current consumption** | | | | | | | | |
| 3.3V total supply current (average) | IVDD3V3_TOTAL_AVG | - | 82.35 | - | mA | - | - | Sum of analog + digital |
| 3.3V digital supply current (average) | IVDD3V3_DIG_AVG | 14.45 | 18.6 | 28 | mA | 20 | 100 | Channel combines DIG+PLL |
| 3.3V analog supply current (average) | IVDD3V3_ANA_AVG | - | 49.8 | - | mA | 40 | 60 | Active mode measurement |
| 3.3V PLL supply current (average) | IVDD3V3_PLL_AVG | - | 13.93 | - | mA | - | - | Included in DIG, no separate Power supply channel |
| **Power consumption** | | | | | | | | |
| Total power consumption | - | - | 271.55 | - | mW | - | - | Derived from IDD x VDD |
| **Logic level inputs (GPIO)** | | | | | | | | |
| VIL (GPIO input low threshold) | VIL | 390 | 470 | 635 | mV | 390 | 635 | - |
| VIH (GPIO input high threshold) | VIH | 443 | 550 | 715 | mV | 443 | 715 | - |
| Hysteresis (GPIO) | Hysteresis | 38 | 80 | 117 | mV | 38 | 117 | - |
| **Logic level inputs (Video pins)** | | | | | | | | |
| VIL (Video input low threshold) | VIL | 1.147 | 1.328 | 1.689 | V | 1.147 | 1.689 | - |
| VIH (Video input high threshold) | VIH | 1.482 | 1.714 | 2.282 | V | 1.482 | 2.282 | - |
| Hysteresis (Video) | Hysteresis | 309 | 387 | 593 | mV | 38 | 593 | - |
| **Data rates** | | | | | | | | |
| Parallel video data rate | DRin,par | - | - | 100 | MHz | pass/fail | | Functional test |
| **Crystal oscillator** | | | | | | | | |
| Crystal frequency | fXTAL | 10 | 20 | 40 | MHz | 19.5 | 20.5 | - |
| **CAM LDO outputs** | | | | | | | | |
| VDD1V8_CAM supply voltage | V_VDD1V8_CAM | 1.7 | 1.8 | 1.9 | V | 1.2 | 2.4 | - |
| VDD1V2_CAM reference voltage | V_VDD1V2_CAM | 1.15 | 1.2 | 1.25 | V | 1.15 | 1.25 | - |

### MAG-PSU00001-NP (10W Synchronous Step-Down DC/DC Converter)

*Table: MAG-PSU00001-NP Key Specifications*

| Parameter | Datasheet Label | DS Min | DS Typ | DS Max | Unit | LSL | USL | Comment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Power** | | | | | | | | |
| Input voltage supply range | PVin, Vin | 5 | - | 11 | V | - | - | Test condition |
| Output current (PCB in air) | Iout | - | - | 1 | A | - | - | Test condition |
| Output power (PCB in air) | Pout | - | - | 2 | W | - | - | Test condition |
| **PWM** | | | | | | | | |
| Maximum Duty Cycle | DMax | - | 100 | - | % | - | - | Cannot be measured, sensitive node |
| Minimum Duty Cycle | DMin | - | 0 | - | % | - | - | Cannot be measured, sensitive node |
| **Error Amplifier** | | | | | | | | |
| DC Gain | DCG | - | 90 | - | dB | - | - | Cannot be measured, sensitive node |
| Unity Gain-Bandwidth | UGBW | - | 20 | - | MHz | - | - | Cannot be measured, sensitive node |
| Slew Rate | SR | - | 10 | - | V/us | - | - | Cannot be measured, sensitive node |
| **Under-voltage lockout** | | | | | | | | |
| Vin start threshold | VinStartTh | - | 4.79 | - | V | 4.4 | 4.8 | - |
| Vin stop threshold | VinStopTh | - | 4.52 | - | V | 4.12 | 4.53 | - |
| **Enable** | | | | | | | | |
| Enable start threshold | EnStartTh | - | 815 | - | mV | 770 | 900 | - |
| Enable stop threshold | EnStopTh | - | 730 | - | mV | 670 | 780 | - |
| Enable pin series resistance | EnSerRes | - | 10 | - | kΩ | - | - | Guaranteed by design |
| **Protections** | | | | | | | | |
| Over Current Protection peak level | OCPpk | - | 6 | - | A | - | - | Cannot be triggered with test setup, functionality of OCP is not covered within test plan |
| Over Current Protection average level | OCPavg | - | 4.8 | - | A | - | - | Cannot be triggered with test setup, functionality of OCP is not covered within test plan |
| Over Temperature start threshold | OTPStartTh | - | 103 | - | °C | - | - | Only tested during characterization |
| Over Temperature stop threshold | OTPStopTh | - | 73 | - | °C | - | - | Only tested during characterization |
| **Soft Start** | | | | | | | | |
| Soft Start duration | SSt | - | - | 440 | us | - | 1500 | - |
| **Power Good** | | | | | | | | |
| Output Over Voltage PGood threshold | OV | - | +6.5 | - | % | 2.5 | 10.5 | - |
| Output Under Voltage PGood threshold | UV | - | -6.5 | - | % | -10.5 | -2.5 | - |
| **PTAT** | | | | | | | | |
| PTAT temperature slope | PTAT | - | 8.5 | - | mV/°C | - | - | Only tested during characterization |

### MAG-VIS100xx-N (Electronic Vision Module)

*Table: MAG-VIS100xx-N Key Specifications*

| Parameter | Datasheet Label | DS Min | DS Typ | DS Max | Unit | Comment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Electrical characteristics** | | | | | | |
| Module supply current | I_SUPPLY_9V | 160 | - | 257 | mA | - |
| AC output impedance (HD-BNC) | Z_out_AC | - | 75 | - | Ohm | - |

---

## References

*Table: Reference Documents*

| Document Name | Version |
| :--- | :--- |
| MAG-IMG002x1-NC Datasheet | Rev. 1.2 (December 2025) |
| MAG-CXP00002-NP Datasheet | Rev. 2.1 (November 2025) |
| MAG-PSU00001-NP Datasheet | Rev. 0.5 (May 2025) |
| MAG-VIS100xx-N Datasheet | Rev. 1.1 (November 2025) |

---

## Glossary / Abbreviations

| Abbreviation | Definition |
| :--- | :--- |
| ADC | Analog-to-Digital Converter |
| ATE | Automatic Test Equipment |
| CONN | Connectivity Test |
| CT | Cold Temperature |
| CXP | CoaXPress (high-speed serial interface standard) |
| DC | Dark Current |
| DCF | Device Configuration File |
| DCNU | Dark Current Non-Uniformity |
| DSNU | Dark Signal Non-Uniformity |
| ESD | Electrostatic Discharge |
| FHD | Full High Definition (1920 x 1080) |
| FPN | Fixed Pattern Noise |
| FPS | Frames Per Second |
| FT | Final Test |
| GPIO | General Purpose Input/Output |
| HD | High Definition (1280 x 720) |
| HT | High Temperature |
| LDO | Low Dropout Regulator |
| LSL | Lower Specification Limit |
| MFT | Module Final Test |
| NVM | Non-Volatile Memory |
| OT | Optical Test |
| OTP | One-Time Programmable (memory) |
| PCB | Printed Circuit Board |
| PLL | Phase-Locked Loop |
| PRNU | Photo Response Non-Uniformity |
| PTAT | Proportional To Absolute Temperature |
| PTC | Photon Transfer Curve |
| ROI | Region Of Interest |
| RT | Room Temperature |
| SMU | Source Measure Unit |
| SN | Spatial Non-uniformity |
| SPC | Statistical Process Control |
| SPI | Serial Peripheral Interface |
| TPG | Test Pattern Generator |
| TRIM | Trimming (calibration of internal references) |
| USL | Upper Specification Limit |
| UVLO | Under-Voltage Lock-Out |
| VCO | Voltage-Controlled Oscillator |
| VER | Functional Verification (module test stage) |
| VGA | Video Graphics Array (640 x 480) |
| VI | Visual Inspection |
| VIS | Vision Sub-board Test |

