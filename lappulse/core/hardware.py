import psutil
import json
import os
import time

class HardwareMonitor:
    def __init__(self):
       
        self.db_path = "lappulse_data.json"
        self.init_database()

    def init_database(self):
        
        if not os.path.exists(self.db_path):
            default_data = {
                "continuous_full_charge_seconds": 0,
                "last_checked_time": time.time()
            }
            with open(self.db_path, "w") as f:
                json.dump(default_data, f)

    def get_system_metrics(self):
        battery = psutil.sensors_battery()
        battery_pct = battery.percent if battery else 0
        is_plugged = battery.power_plugged if battery else False
        cpu_usage = psutil.cpu_percent(interval=None)
        
        
        should_notify = self.track_battery_maintenance(battery_pct, is_plugged)
        
        return {
            "battery_percent": battery_pct,
            "is_plugged": is_plugged,
            "cpu_usage": cpu_usage,
            "trigger_discharge_alert": should_notify
        }

    def track_battery_maintenance(self, percent, is_plugged):
        
        with open(self.db_path, "r") as f:
            data = json.load(f)
        
        current_time = time.time()
        time_diff = current_time - data["last_checked_time"]
        data["last_checked_time"] = current_time
        
        should_notify = False

        
        if is_plugged and percent >= 100:
            data["continuous_full_charge_seconds"] += time_diff
            
            
            #30 days = 2,592,000 seconds
            if data["continuous_full_charge_seconds"] >= 30: 
                should_notify = True
        else:
            
            data["continuous_full_charge_seconds"] = 0

        
        with open(self.db_path, "w") as f:
            json.dump(data, f)
            
        return should_notify