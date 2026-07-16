import json
import os
from flask import Blueprint, jsonify, request
from ai.decision_engine import DecisionEngine
from ai.rag_engine import RAGEngine
from simulator.crowd_generator import CrowdGenerator
from simulator.transport_generator import TransportGenerator
from simulator.incident_generator import IncidentGenerator
from database.models import db, SensorReading

dashboard_bp = Blueprint("dashboard", __name__)
rag = RAGEngine()
decision_engine = DecisionEngine()
crowd_gen = CrowdGenerator()
transport_gen = TransportGenerator()
incident_gen = IncidentGenerator()


def _sync_stadium():
    stadium_id = request.args.get("stadium_id") or (request.get_json(silent=True) or {}).get("stadium_id")
    if stadium_id and stadium_id != rag.stadium_id:
        rag.set_stadium(stadium_id)

def load_sensor_data():
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "..", "data", "live_sensor.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"gates": []}


@dashboard_bp.route("/api/dashboard/overview", methods=["GET"])
def overview():
    _sync_stadium()
    sensor_data = load_sensor_data()
    gates = sensor_data.get("gates", [])
    incidents = sensor_data.get("incidents", {})
    transport = sensor_data.get("transport", {})

    total_density = sum(g.get("density", 0) for g in gates)
    avg_density = round(total_density / max(len(gates), 1), 1)
    total_visitors = sensor_data.get("total_visitors", 0)

    critical_gates = [g for g in gates if g.get("status") == "critical"]
    warning_gates = [g for g in gates if g.get("status") == "warning"]

    active_alerts = len(critical_gates) + len(warning_gates)
    medical_requests = incidents.get("active_medical", 0)
    security_alerts = incidents.get("security_alerts", 0)

    shuttle_info = transport.get("shuttle_buses", {})
    parking = transport.get("parking", {})

    stadium_ctx = rag.get_stadium_context()

    return jsonify({
        "total_visitors": total_visitors,
        "avg_density": avg_density,
        "crowd_level": "high" if avg_density > 60 else "medium" if avg_density > 30 else "low",
        "active_alerts": active_alerts,
        "critical_gates": len(critical_gates),
        "warning_gates": len(warning_gates),
        "medical_requests": medical_requests,
        "security_alerts": security_alerts,
        "shuttle_buses": shuttle_info,
        "parking": parking,
        "gates": gates,
        "stadium": {
            "name": stadium_ctx["name"],
            "location": stadium_ctx["location"],
            "capacity": stadium_ctx["capacity"],
        },
    })


@dashboard_bp.route("/api/dashboard/gates", methods=["GET"])
def gate_monitoring():
    _sync_stadium()
    sensor_data = load_sensor_data()
    gates = sensor_data.get("gates", [])

    gate_details = []
    for gate in gates:
        analysis = decision_engine.generate_alert(gate)
        gate_details.append({
            "gate": gate.get("gate"),
            "density": gate.get("density"),
            "queue_time": gate.get("queue_time"),
            "crowd_flow": gate.get("crowd_flow"),
            "status": gate.get("status"),
            "alert": analysis,
        })

    return jsonify({"gates": gate_details})


@dashboard_bp.route("/api/dashboard/ai-analysis", methods=["GET"])
def ai_analysis():
    _sync_stadium()
    sensor_data = load_sensor_data()
    analysis = decision_engine.analyze_crowd(sensor_data)
    return jsonify(analysis)


@dashboard_bp.route("/api/dashboard/refresh", methods=["POST"])
def refresh_data():
    crowd_data = crowd_gen.generate()
    transport_data = transport_gen.generate()
    incident_data = incident_gen.generate()

    for gate in crowd_data.get("gates", []):
        reading = SensorReading(
            gate=gate.get("gate"),
            density=gate.get("density"),
            queue_time=gate.get("queue_time"),
            crowd_flow=gate.get("crowd_flow"),
            status=gate.get("status"),
        )
        db.session.add(reading)
    db.session.commit()

    return jsonify({
        "status": "success",
        "crowd": crowd_data,
        "transport": transport_data,
        "incidents": incident_data,
    })


@dashboard_bp.route("/api/dashboard/stadium", methods=["GET"])
def dashboard_stadium():
    _sync_stadium()
    return jsonify({"stadium": rag.get_stadium_context()})

@dashboard_bp.route("/api/dashboard/sensor-history", methods=["GET"])
def sensor_history():
    readings = SensorReading.query.order_by(
        SensorReading.timestamp.desc()
    ).limit(100).all()
    return jsonify([r.to_dict() for r in readings])
