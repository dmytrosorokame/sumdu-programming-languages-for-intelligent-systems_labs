"""Knowledge base and inference engine for the PC Diagnostic Expert System."""
import pandas as pd


# Knowledge base: rules mapping symptoms to diagnoses and recommendations
RULES_DATA = {
    "rule_id": list(range(1, 21)),
    "symptom_1": [
        "pc_not_turning_on", "pc_not_turning_on", "pc_not_turning_on",
        "blue_screen", "blue_screen",
        "slow_performance", "slow_performance", "slow_performance",
        "no_display", "no_display",
        "strange_noises", "strange_noises",
        "overheating", "overheating",
        "internet_not_working", "internet_not_working",
        "usb_not_recognized", "usb_not_recognized",
        "random_restarts", "random_restarts",
    ],
    "symptom_2": [
        "no_lights", "fans_spinning", "lights_on_no_boot",
        "after_driver_update", "random_bsod",
        "high_cpu_usage", "low_ram", "slow_boot",
        "monitor_black", "artifacts_on_screen",
        "clicking_hdd", "buzzing_fan",
        "high_cpu_temp", "dust_buildup",
        "no_wifi_icon", "wifi_connected_no_internet",
        "device_not_listed", "device_disconnects",
        "under_load", "at_idle",
    ],
    "diagnosis": [
        "Power supply failure",
        "Motherboard failure",
        "Boot drive failure",
        "Driver incompatibility",
        "RAM failure",
        "Malware or background processes",
        "Insufficient RAM",
        "Too many startup programs",
        "GPU or cable failure",
        "GPU overheating or failure",
        "Hard drive failing",
        "Fan bearing failure",
        "CPU cooler issue",
        "Dust accumulation",
        "Network adapter disabled",
        "DNS or router issue",
        "USB port or driver issue",
        "USB power or cable issue",
        "PSU insufficient wattage",
        "Motherboard or PSU instability",
    ],
    "recommendation": [
        "Test with a different power supply or check the power cable connection.",
        "Inspect the motherboard for burnt components; consider replacement.",
        "Check the boot order in BIOS and test the drive on another PC.",
        "Roll back the recently installed driver via Safe Mode.",
        "Run Windows Memory Diagnostic or test RAM sticks individually.",
        "Run a full antivirus scan and check Task Manager for heavy processes.",
        "Upgrade RAM or close unused applications to free memory.",
        "Disable unnecessary startup programs in Task Manager > Startup tab.",
        "Try a different cable or test with another monitor; reseat GPU.",
        "Monitor GPU temperature; clean the heatsink and replace thermal paste.",
        "Back up data immediately and replace the hard drive.",
        "Replace the noisy fan before it fails completely.",
        "Reapply thermal paste and ensure the cooler is properly mounted.",
        "Clean the PC internals with compressed air; improve airflow.",
        "Enable the network adapter in Device Manager or Network Settings.",
        "Restart the router; try changing DNS to 8.8.8.8 or 1.1.1.1.",
        "Try a different USB port; reinstall USB drivers in Device Manager.",
        "Use a shorter or higher-quality USB cable; check power output.",
        "Calculate total system power draw and upgrade PSU if needed.",
        "Test with a known-good PSU; check motherboard capacitors.",
    ],
}

# Symptom categories with human-readable labels
SYMPTOM_CATEGORIES = {
    "pc_not_turning_on": "PC does not turn on",
    "blue_screen": "Blue screen of death (BSOD)",
    "slow_performance": "Slow performance",
    "no_display": "No display / video issues",
    "strange_noises": "Strange noises from PC",
    "overheating": "Overheating",
    "internet_not_working": "Internet not working",
    "usb_not_recognized": "USB device not recognized",
    "random_restarts": "Random restarts",
}

SECONDARY_SYMPTOMS = {
    "pc_not_turning_on": {
        "no_lights": "No lights or fans at all",
        "fans_spinning": "Fans spin but no display",
        "lights_on_no_boot": "Lights on, fans work, but system does not boot",
    },
    "blue_screen": {
        "after_driver_update": "Appeared after a driver update",
        "random_bsod": "Appears randomly without clear cause",
    },
    "slow_performance": {
        "high_cpu_usage": "CPU usage is constantly high",
        "low_ram": "RAM usage is above 90%",
        "slow_boot": "System takes very long to boot",
    },
    "no_display": {
        "monitor_black": "Monitor is completely black",
        "artifacts_on_screen": "Visual artifacts / glitches on screen",
    },
    "strange_noises": {
        "clicking_hdd": "Clicking sounds from hard drive area",
        "buzzing_fan": "Buzzing or grinding from a fan",
    },
    "overheating": {
        "high_cpu_temp": "CPU temperature is above 90°C",
        "dust_buildup": "Visible dust inside the case",
    },
    "internet_not_working": {
        "no_wifi_icon": "Wi-Fi icon is missing or shows disabled",
        "wifi_connected_no_internet": "Connected to Wi-Fi but no internet access",
    },
    "usb_not_recognized": {
        "device_not_listed": "Device does not appear in Device Manager",
        "device_disconnects": "Device connects but keeps disconnecting",
    },
    "random_restarts": {
        "under_load": "Restarts happen under heavy load (gaming, rendering)",
        "at_idle": "Restarts happen even at idle",
    },
}


class DiagnosticSystem:
    """Inference engine for the PC diagnostic expert system."""

    def __init__(self):
        self.knowledge_base = pd.DataFrame(RULES_DATA)

    def diagnose(self, primary_symptom, secondary_symptom):
        """Find matching rules based on selected symptoms."""
        result = self.knowledge_base[
            (self.knowledge_base["symptom_1"] == primary_symptom)
            & (self.knowledge_base["symptom_2"] == secondary_symptom)
        ]
        return result

    def get_all_rules(self):
        """Return the full knowledge base."""
        return self.knowledge_base
