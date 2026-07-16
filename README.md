# Software-Defined Universal Transducer Matrix (SD-UTM)
### Advanced Phase-Delay Architecture (APDA-Core)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![System State](https://img.shields.io/badge/System__State-STANDBY-green.svg)]()
[![Hardware Verification](https://img.shields.io/badge/HIL__Verification-PASSED-brightgreen.svg)]()

An open-source systems architecture for a non-invasive, highly automated therapeutic platform utilizing advanced acoustic and crossed electromagnetic energy convergence. The system dynamically matches tissue acoustic impedance, auto-isolates hardware micro-faults, and operates under strict biological boundaries to safely execute lithotripsy, thrombolysis, and tumor ablation without surgical entry.

---

## 📂 Repository Structure
* `/config/system_architecture.json` - Static system constraints, array geometry coordinates, and FMEA tripwire thresholds.
* `/src/hil_test_bench.py` - Hardware-in-the-Loop simulation testing hardware sweeps, client exclusion logic, and Level-4 microsecond trips.
* `LICENSE` - GNU General Public License v3.0 core terms.

---

## 🛠️ Core Engineering Features

### 1. Dynamic Energy Matrix
* **2,048 CMUT Elements:** Configured in a concentric Fibonacci-spaced spherical cap (35 cm base, 22 cm height) delivering focused acoustic pressure waves (500 kHz – 5 MHz).
* **512 Nested Micro-EM Coils:** Intersecting inductive channels delivering high-velocity transient electric fields (100 V/cm to 1000 V/cm) for mechanical clot disruption and localized electroporation.

### 2. Intelligent AI Hibernation
The system leverages symbolic regression to determine standard spatial tissue paths. Once baseline calibration equations are established, the NPU transitions into a low-power hibernation loop—reducing peak consumption from **120 W** to a steady state of **< 8.5 W**, running purely on analog phase-locked tracking loops.

### 3. Microsecond-Level Fail-Passive FMEA
A hardware-level comparator bus monitors return signals from embedded Passive Cavitation Detectors (PCD) and Diffuse Optical Tomography (DOT) grids. If any parameter crosses the biological safety thresholds (e.g., adjacent healthy tissue reaching **41.0°C**), solid-state isolation relays open in **< 20 microseconds**, instantly de-energizing the Class-D high-voltage rails.

---

## 📈 Biological Bounding Reference

| Therapeutic Module | Non-Invasive Metric Ceiling | Excretion / Processing Channel |
| :--- | :--- | :--- |
| **Lithotripsy** | Stone Diameter ≤ 12.0 mm | Natural Renal/Urinary Flow (< 1.5 mm sand fragments) |
| **Thrombolysis** | Clot Length ≤ 40.0 mm | Hepatic/Splenic Filter Processing |
| **Tumor Ablation** | Slurry Volume ≤ 100.0 mL | Lymphatic System Resorption |

---

## 🚀 Running the Hardware Test Bench
To verify the system's runtime fault isolation and scenario handlers, execute the integrated Hardware-in-the-Loop simulation:

```bash
python src/hil_test_bench.py
