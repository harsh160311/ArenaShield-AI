import random
import time


class SustainabilityEngine:
    def __init__(self):
        self._seed = int(time.time() % 1000)

    def get_status(self):
        random.seed(self._seed + int(time.time() // 30))
        return {
            "energy_optimization": random.randint(72, 96),
            "waste_bins": self._waste_status(),
            "water_consumption": random.randint(55, 90),
            "carbon_footprint": random.choice(["low", "medium", "low"]),
            "ai_suggestion": random.choice([
                "Deploy cleaning team in Zone C - bin at 92% capacity",
                "Reduce concourse lighting by 20% - crowd density low",
                "Water consumption within normal range - no action needed",
                "Solar panels at 94% efficiency - optimal conditions",
                "Redirect cleaning crew to Gate B area",
            ]),
        }

    def _waste_status(self):
        bins = []
        for gate in ["A", "B", "C", "D"]:
            bins.append({
                "gate": gate,
                "fill_level": random.randint(30, 95),
                "status": "full" if random.random() > 0.7 else "available",
            })
        return bins
