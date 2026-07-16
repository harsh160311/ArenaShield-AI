import random
import json
import os


class CrowdGenerator:
    def __init__(self):
        self.gates = ["A", "B", "C", "D"]
        self.base_density = {"A": 45, "B": 50, "C": 30, "D": 40}
        self.base_queue = {"A": 8, "B": 12, "C": 5, "D": 10}

    def generate(self):
        readings = []
        for gate in self.gates:
            density_change = random.randint(-10, 15)
            new_density = max(5, min(100, self.base_density[gate] + density_change))

            queue_change = random.randint(-3, 5)
            new_queue = max(1, self.base_queue[gate] + queue_change)

            if new_density >= 80:
                status = "critical"
                flow = "surge"
            elif new_density >= 50:
                status = "warning"
                flow = "increasing" if density_change > 0 else "stable"
            else:
                status = "normal"
                flow = "stable" if abs(density_change) < 5 else "increasing"

            readings.append({
                "gate": gate,
                "density": new_density,
                "queue_time": new_queue,
                "crowd_flow": flow,
                "status": status,
            })

            self.base_density[gate] = new_density
            self.base_queue[gate] = new_queue

        total_visitors = sum(
            int(r["density"] * random.uniform(450, 550)) for r in readings
        )
        total_visitors = max(10000, min(80000, total_visitors))

        sensor_data = {"gates": readings, "total_visitors": total_visitors}

        base = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base, "..", "data", "live_sensor.json")

        try:
            with open(path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing = {}

        existing["gates"] = readings
        existing["total_visitors"] = total_visitors

        with open(path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)

        return sensor_data
