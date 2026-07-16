import random
import json
import os
from datetime import datetime


class IncidentGenerator:
    def generate(self):
        active_medical = random.choices([0, 1, 2, 3], weights=[40, 30, 20, 10])[0]
        security_alerts = random.choices([0, 0, 0, 1], weights=[60, 20, 15, 5])[0]
        maintenance_requests = random.choices([0, 1, 2, 3], weights=[30, 35, 25, 10])[0]

        incidents = {
            "active_medical": active_medical,
            "security_alerts": security_alerts,
            "maintenance_requests": maintenance_requests,
            "generated_at": datetime.utcnow().isoformat(),
        }

        base = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base, "..", "data", "live_sensor.json")

        try:
            with open(path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing = {}

        existing["incidents"] = incidents

        with open(path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)

        return incidents
