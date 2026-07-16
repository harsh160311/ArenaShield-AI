import random
import json
import os


class TransportGenerator:
    def generate(self):
        total_buses = 20
        operational = random.randint(10, total_buses)
        en_route = random.randint(2, 6)
        waiting = max(0, operational - en_route - random.randint(2, 4))

        parking_lots = {
            "lot_a": {
                "capacity": 2000,
                "filled": random.randint(200, 800),
            },
            "lot_b": {
                "capacity": 1500,
                "filled": random.randint(800, 1400),
            },
            "lot_c": {
                "capacity": 1800,
                "filled": random.randint(500, 1200),
            },
        }

        for lot in parking_lots.values():
            ratio = lot["filled"] / lot["capacity"]
            if ratio >= 0.85:
                lot["status"] = "full"
            elif ratio >= 0.50:
                lot["status"] = "filling"
            else:
                lot["status"] = "available"

        transport_data = {
            "shuttle_buses": {
                "operational": operational,
                "en_route": en_route,
                "waiting": waiting,
            },
            "parking": parking_lots,
        }

        base = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base, "..", "data", "live_sensor.json")

        try:
            with open(path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing = {}

        existing["transport"] = transport_data

        with open(path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)

        return transport_data
