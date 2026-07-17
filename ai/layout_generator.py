import json
import os
import random

BASE = os.path.dirname(os.path.abspath(__file__))
DETAILED_PATH = os.path.join(BASE, "..", "data", "stadium.json")
STADIUMS_PATH = os.path.join(BASE, "..", "data", "stadiums.json")


def _load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _get_stadium_name(stadium_id):
    data = _load_json(STADIUMS_PATH)
    for s in data.get("stadiums", []):
        if s.get("id") == stadium_id:
            return s.get("name", f"Stadium {stadium_id}")
    return "ArenaShield National Stadium"


def generate_stadium_layout(stadium_id):
    detailed = _load_json(DETAILED_PATH)
    template = detailed.get("stadium", {})
    gates = detailed.get("gates", [])
    blocks = detailed.get("seating_blocks", [])
    medical = detailed.get("medical_rooms", [])
    food = detailed.get("food_zones", [])
    washrooms = detailed.get("washrooms", [])
    exits = detailed.get("emergency_exits", [])
    accessibility = detailed.get("accessibility", {})

    random.seed(hash(stadium_id) % (2**31))
    gate_labels = ["A", "B", "C", "D"]
    sections = ["North", "East", "South", "West"]

    generated_gates = []
    for i, label in enumerate(gate_labels):
        gate = None
        for g in gates:
            if g.get("id", "").endswith(f"Gate {label}") or g.get("id", "").endswith(label):
                gate = g
                break
        if gate is None:
            section = sections[i] if i < len(sections) else f"Section {i}"
            gate = {
                "id": f"Gate {label}",
                "name": f"{section} Entrance",
                "section": section,
                "accessible": True,
                "nearby_blocks": [f"{label}{j}" for j in range(1, 11)],
                "amenities": ["Ticket Counter", "First Aid", "Washroom"],
            }
        generated_gates.append(gate)

    generated_blocks = []
    for label in gate_labels:
        block = None
        for b in blocks:
            if b.get("gate", "").endswith(f"Gate {label}") or b.get("gate", "").endswith(label):
                block = b
                break
        if block is None:
            block = {
                "id": f"{label}1-{label}10",
                "section": sections[gate_labels.index(label)] if gate_labels.index(label) < len(sections) else "General",
                "gate": f"Gate {label}",
                "rows": 25,
                "seats_per_row": 20,
            }
        generated_blocks.append(block)

    generated_medical = []
    for room in medical:
        generated_medical.append({
            "id": room.get("id", room.get("name", "Medical Center")),
            "location": room.get("location", "Main Concourse"),
            "block": room.get("block", "Central"),
            "level": room.get("level", "Ground"),
            "staff": room.get("staff", "Available"),
        })
    if not generated_medical:
        generated_medical = [
            {"id": "First Aid East", "location": "Gate B", "block": "East Block", "level": "Ground", "staff": "Available"},
            {"id": "Medical Center West", "location": "Gate D", "block": "West Block", "level": "Ground", "staff": "Available"},
            {"id": "Main Medical Suite", "location": "North Concourse", "block": "North Block", "level": "1st Floor", "staff": "Full Team"},
        ]

    generated_food = []
    for z in food:
        generated_food.append({
            "id": z.get("id", "Food Court"),
            "location": z.get("location", "Central Plaza"),
            "cuisines": z.get("cuisines", ["Burgers", "Pizza", "Beverages"]),
            "seating": z.get("seating", 200),
        })
    if not generated_food:
        generated_food = [
            {"id": "Central Food Court", "location": "Central Plaza", "cuisines": ["Burgers", "Pizza", "Asian"], "seating": 400},
            {"id": "North Concession", "location": "Block A Concourse", "cuisines": ["Hot Dogs", "Nachos"], "seating": 100},
        ]

    generated_washrooms = []
    for w in washrooms:
        generated_washrooms.append({
            "id": w.get("id", "WR"),
            "location": w.get("location", "Gate Area"),
            "block": w.get("block", "Main"),
            "accessible": w.get("accessible", True),
            "family": w.get("family", False),
        })
    if not generated_washrooms:
        for label in gate_labels:
            generated_washrooms.extend([
                {"id": f"WR-{label}1", "location": f"Gate {label}", "block": sections[gate_labels.index(label)], "accessible": True, "family": True},
                {"id": f"WR-{label}2", "location": f"Block {label}", "block": sections[gate_labels.index(label)], "accessible": True, "family": False},
            ])

    generated_exits = []
    for ex in exits:
        generated_exits.append({
            "id": ex.get("id", "EX"),
            "location": ex.get("location", "Gate Area"),
            "capacity": ex.get("capacity", 500),
        })
    if not generated_exits:
        for i, label in enumerate(gate_labels):
            generated_exits.append({"id": f"EX-0{i+1}", "location": f"Gate {label} {sections[i]}", "capacity": 500})
        generated_exits.append({"id": "EX-05", "location": "Central Plaza", "capacity": 300})

    generated_accessibility = accessibility if accessibility else {
        "wheelchair_routes": ["All gates have ramp access", "Elevators at all concourses"],
        "special_assistance": "Available at all gates and information desks",
        "accessible_seating": [f"Block {label}: Rows 1-2" for label in gate_labels],
        "service_animals": "Welcome throughout the stadium",
    }

    name = _get_stadium_name(stadium_id)
    capacity = None
    for s in _load_json(STADIUMS_PATH).get("stadiums", []):
        if s.get("id") == stadium_id:
            capacity = s.get("capacity")
            break

    return {
        "name": name,
        "capacity": capacity or 80000,
        "location": template.get("location", "Sports City"),
        "gates": generated_gates,
        "seating_blocks": generated_blocks,
        "medical_rooms": generated_medical,
        "food_zones": generated_food,
        "washrooms": generated_washrooms,
        "emergency_exits": generated_exits,
        "accessibility": generated_accessibility,
    }
