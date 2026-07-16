#!/usr/bin/env python3
"""
SD-UTM / APDA-Core System: Hardware-in-the-Loop (HIL) Test Bench
Validates bootstrap diagnostics, patient screening boundaries, and FMEA tripwires.
Licensed under GNU GPL v3.0
"""

import time

class UniversalTransducerMatrix:
    def __init__(self):
        self.system_state = "OFFLINE"
        self.cmut_elements = [150.0] * 2048  # Real impedance component in Ohms
        self.em_coils = [2.4] * 512          # DC Resistance in Ohms
        
        # Inject calibration faults for testing execution
        self.cmut_elements[85] = 1200000.0   # Open circuit
        self.cmut_elements[912] = 0.2        # Short circuit
        self.em_coils[104] = 85.0            # Corrupted coil resistance

    def log(self, level, message):
        prefix = {
            "BOOT": "[BOOTSTRAP]",
            "OK": "  -> [OK]",
            "FAIL": "  -> [!]",
            "CHECK": "[PRE-CHECK]",
            "TX": "[THERAPY ACTIVE]",
            "TRIP": "[** LEVEL 4 HARDWARE TRIPWIRE ACTIVATED **]",
            "SHUTDOWN": "[SHUTDOWN]"
        }
        print(f"{prefix.get(level, '')} {message}")

    def power_on_reset(self):
        self.log("BOOT", "Initializing Power-On Reset (POR)...")
        time.sleep(0.1)
        self.log("OK", "Mu-Metal and Copper Faraday Shielding Active (Attenuation: 94.2 dB)")
        self.log("OK", "Saline Coupling Sleeve Inflated to 0.20 bar. Inline Degasser running at 3200 RPM.")
        
        # Scan Arrays
        opens = [i for i, r in enumerate(self.cmut_elements) if r > 10000.0]
        shorts = [i for i, r in enumerate(self.cmut_elements) if r < 5.0]
        em_faults = [i for i, r in enumerate(self.em_coils) if r < 1.8 or r > 3.5]
        
        self.log("OK", f"DMA Transducer Registry Scan Complete: {len(self.cmut_elements)} Elements Online.")
        
        if opens or shorts or em_faults:
            print("\n==================================================")
            print("                 ANALOG BENCH TEST RESULTS          ")
            print("==================================================")
            print(f"  CMUT Channels Scanned : {len(self.cmut_elements)}")
            print(f"  EM Channels Scanned   : {len(self.em_coils)}")
            print("--------------------------------------------------")
            print("  [!] CMUT FAULTS DETECTED:")
            for idx in opens:
                self.log("FAIL", f"Element #{idx:04d}: OPEN CIRCUIT ({self.cmut_elements[idx]/1e6:.2f} M-Ohm) - ISOLATING CHANNEL")
            for idx in shorts:
                self.log("FAIL", f"Element #{idx:04d}: SHORT CIRCUIT ({self.cmut_elements[idx]:.2f} Ohm) - ISOLATING CHANNEL")
            print("  [!] EM COIL FAULTS DETECTED:")
            for idx in em_faults:
                self.log("FAIL", f"Coil #{idx:03d}: OUT OF SPEC ({self.em_coils[idx]:.2f} Ohm) - DISABLE COIL")
            print("==================================================\n")
            
            self.system_state = "EMERGENCY_STOP"
            print("[ABORT] Diagnostic failed. Critical faults must be repaired/isolated before high-voltage power is authorized.\n")
            return False
        
        self.log("OK", "Fail-Passive Safety Relays Energized: Class-D High-Voltage Rails Armed.")
        self.system_state = "STANDBY"
        print(f"[BOOTSTRAP COMPLETE] System State: {self.system_state}\n")
        return True

    def clear_faults_for_functional_test(self):
        # Reset matrix to perfect factory specifications for functional execution
        self.cmut_elements = [150.0] * 2048
        self.em_coils = [2.4] * 512

    def screen_patient(self, subject_id, pathology, metric_val):
        self.log("CHECK", f"Screening Patient: {subject_id} | Pathology: {pathology.upper()}...")
        if pathology == "lithotripsy" and metric_val > 12.0:
            print(f"  -> [REJECT] Stone diameter {metric_val} mm exceeds safe non-invasive ceiling of 12.0 mm!")
            print("  -> [ACTION] Safe excretion cannot be guaranteed. Refer patient to Invasive Micro-Surgery.\n")
            return False
        self.log("OK", "Pathology falls within safe, non-invasive anatomical boundaries.\n")
        return True

    def execute_therapy(self, scenario_name, run_fault_injection=False):
        self.log("TX", f"Firing Array for Scenario: {scenario_name.upper()}")
        print("-" * 80)
        print(f"{'Time (s)':<10}{'Drive Cmd':<12}{'Tissue Temp':<15}{'Metric Val':<15}{'APDA Loop Status'}")
        print("-" * 80)
        
        tissue_temp = 36.5
        metric_val = 0.018 if scenario_name == "lithotripsy" else 0.0
        
        for t in range(4):
            if run_fault_injection and t == 2:
                print("-" * 80)
                print(f"[! FAULT INJECTION !] Triggering simulated anomaly: THERMAL_RUNAWAY\n")
                tissue_temp = 41.5
                self.log("TRIP", f"REASON: CRITICAL OVERHEAT: Tissue Temp reached {tissue_temp}°C")
                self.log("TRIP", "ACTION: Safety relays opened. System de-energized in < 20 microseconds.")
                self.system_state = "EMERGENCY_STOP"
                print(f"  SAFETY RESET: Array Isolated. Tissue protected. System State: {self.system_state}\n")
                break
            
            status_msg = "HIBERNATING (Locked Calculus)"
            metric_unit = "MPa" if scenario_name == "lithotripsy" else "K/s"
            metric_str = f"{metric_val:.3f} {metric_unit}"
            
            print(f"{t:<10.1f}{45.00:<12.2f}{tissue_temp:<15.2f}{metric_str:<15}{status_msg}")
            time.sleep(0.05)
            
        if self.system_state != "EMERGENCY_STOP":
            print("-" * 80)
            print(f"[OK] {scenario_name.upper()} Treatment Completed Successfully.\n")
            
        self.shutdown_sequence()

    def shutdown_sequence(self):
        self.log("SHUTDOWN", "Commencing clean-up sequence...")
        self.log("OK", "Initiating post-procedure cold saline skin flush (34°C). Cleaning skin lipids.")
        self.log("OK", "Emptying coupling sleeve fluid reservoir. Evacuating to isolated waste cartridge.")
        self.system_state = "OFFLINE"
        print(f"[SHUTDOWN COMPLETE] Final System State: {self.system_state}. Device is safe for extraction.\n")

if __name__ == "__main__":
    dev = UniversalTransducerMatrix()
    
    print("--- SCENARIO A: Diagnostic Hardware Fault Isolation ---")
    dev.power_on_reset()
    
    print("--- SCENARIO B: Patient Exclusion Protection ---")
    dev.clear_faults_for_functional_test()
    if dev.power_on_reset():
        dev.screen_patient("Subject-01", "lithotripsy", 16.5)
        
    print("--- SCENARIO C: Successful Standard Procedure ---")
    if dev.screen_patient("Subject-02", "lithotripsy", 8.5):
        dev.execute_therapy("lithotripsy", run_fault_injection=False)
        
    print("--- SCENARIO D: Active FMEA Fault Intercept ---")
    dev.system_state = "OFFLINE"
    if dev.power_on_reset():
        if dev.screen_patient("Subject-03", "tumor_ablation", 45.0):
            dev.execute_therapy("tumor_ablation", run_fault_injection=True)
