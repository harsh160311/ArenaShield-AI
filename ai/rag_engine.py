import json
import os
from ai.vector_store import VectorStore
from ai.layout_generator import generate_stadium_layout


class RAGEngine:
    def __init__(self, stadium_id="arenashield-national"):
        self.stadium_id = stadium_id
        self.stadiums_data = self._load_json("data/stadiums.json")
        self.stadium_data = self._get_stadium_data(stadium_id)
        self.emergency_data = self._load_json("data/emergency.json")
        self.sensor_data = self._load_json("data/live_sensor.json")
        self.vector_store = VectorStore()

    def _load_json(self, path):
        try:
            base = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(base, "..", path)
            with open(full_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _get_stadium_data(self, stadium_id):
        stadiums = self.stadiums_data.get("stadiums", [])
        for s in stadiums:
            if s.get("id") == stadium_id:
                return s
        return stadiums[0] if stadiums else {}

    def _get_layout(self, stadium_id):
        return generate_stadium_layout(stadium_id)

    def set_stadium(self, stadium_id):
        self.stadium_id = stadium_id
        self.stadium_data = self._get_stadium_data(stadium_id)
        self.refresh_sensor_data()

    def get_stadium_list(self):
        return [
            {
                "id": s["id"],
                "name": s["name"],
                "location": s.get("location", ""),
                "country": s.get("country", "Other")
            }
            for s in self.stadiums_data.get("stadiums", [])
        ]

    def refresh_sensor_data(self):
        self.sensor_data = self._load_json("data/live_sensor.json")

    def retrieve_context(self, query):
        query = query.lower()
        layout = self._get_layout(self.stadium_id)

        context = {
            "stadium": self.stadium_data,
            "layout": layout,
            "emergency": self.emergency_data,
            "sensors": self.sensor_data,
            "relevant_zones": [],
        }

        gates = layout.get("gates", [])
        for gate in gates:
            gid = gate.get("id", "").lower()
            if gid in query:
                context["relevant_zones"].append({"type": "gate", "data": gate})

        if any(w in query for w in ["medical", "doctor", "hospital", "injury", "hurt", "ayuda"]):
            context["relevant_zones"].append({"type": "medical", "data": layout.get("medical_rooms", [])})
            context["relevant_zones"].append({"type": "emergency", "data": self.emergency_data.get("emergency_contacts", {})})

        if any(w in query for w in ["emergency", "fire", "evacuate", "evacuation"]):
            context["relevant_zones"].append({"type": "emergency", "data": self.emergency_data})

        if any(w in query for w in ["food", "hungry", "restaurant", "concession", "comida", "eat"]):
            context["relevant_zones"].append({"type": "food", "data": layout.get("food_zones", [])})

        if any(w in query for w in ["wheelchair", "accessible", "accessibility", "disability"]):
            context["relevant_zones"].append({"type": "accessibility", "data": layout})

        if any(w in query for w in ["washroom", "bathroom", "toilet", "restroom", "baño"]):
            context["relevant_zones"].append({"type": "washroom", "data": layout.get("washrooms", [])})

        vector_results = self.vector_store.search(query, top_k=3)
        if vector_results:
            context["vector_results"] = vector_results

        return context

    def get_stadium_context(self):
        layout = self._get_layout(self.stadium_id)
        return {
            "name": layout.get("name", self.stadium_data.get("name", "")),
            "location": layout.get("location", self.stadium_data.get("location", "")),
            "capacity": layout.get("capacity", self.stadium_data.get("capacity", 0)),
            "gates": layout.get("gates", []),
            "blocks": layout.get("seating_blocks", []),
            "medical": layout.get("medical_rooms", []),
            "food": layout.get("food_zones", []),
            "emergency_exits": layout.get("emergency_exits", []),
        }

    def get_crowd_summary(self):
        sensors = self.sensor_data.get("gates", [])
        if not sensors:
            return "No live sensor data available."
        summary = []
        for gate in sensors:
            status = gate.get("status", "normal")
            density = gate.get("density", 0)
            summary.append(f"{gate.get('gate', 'Unknown')}: {density}% density ({status})")
        return "\n".join(summary)

    def find_nearest_medical(self, location):
        location = location.lower()
        layout = self._get_layout(self.stadium_id)
        rooms = layout.get("medical_rooms", [])
        for room in rooms:
            if location in room.get("location", "").lower():
                return room
        return rooms[0] if rooms else {"location": "Main Medical Center", "distance": "200m"}

    def find_nearest_exit(self, location):
        location = location.lower()
        layout = self._get_layout(self.stadium_id)
        for gate in layout.get("gates", []):
            if location in gate.get("name", "").lower():
                return gate
        return layout.get("gates", [{}])[0] if layout.get("gates") else {"name": "Gate A"}
