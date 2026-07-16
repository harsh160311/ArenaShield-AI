from flask import Blueprint, jsonify
from database.models import db, Alert
from ai.decision_engine import DecisionEngine
import json
import os

alerts_bp = Blueprint("alerts", __name__)
decision_engine = DecisionEngine()


def load_sensor_data():
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "..", "data", "live_sensor.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"gates": []}


@alerts_bp.route("/api/alerts", methods=["GET"])
def get_alerts():
    active = Alert.query.filter_by(resolved=False)\
        .order_by(Alert.timestamp.desc()).limit(20).all()
    return jsonify([a.to_dict() for a in active])


@alerts_bp.route("/api/alerts/generate", methods=["POST"])
def generate_alerts():
    sensor_data = load_sensor_data()
    gates = sensor_data.get("gates", [])
    new_alerts = []

    for gate in gates:
        density = gate.get("density", 0)
        gate_name = gate.get("gate", "Unknown")
        status = gate.get("status", "normal")

        if status == "critical":
            analysis = decision_engine.generate_alert(gate)
            existing = Alert.query.filter_by(
                gate=gate_name, resolved=False
            ).first()

            if not existing:
                alert = Alert(
                    gate=gate_name,
                    alert_type="crowd_congestion",
                    severity="critical",
                    message=analysis["message"],
                    ai_recommendations=json.dumps(analysis["recommendations"]),
                )
                db.session.add(alert)
                new_alerts.append(gate_name)

        elif status == "warning":
            existing = Alert.query.filter_by(
                gate=gate_name, alert_type="crowd_congestion", resolved=False
            ).first()
            if not existing:
                alert = Alert(
                    gate=gate_name,
                    alert_type="crowd_congestion",
                    severity="warning",
                    message=f"Moderate congestion at {gate_name}. Density at {density}%.",
                    ai_recommendations=json.dumps([
                        f"Monitor {gate_name} closely",
                        "Prepare backup staff",
                    ]),
                )
                db.session.add(alert)
                new_alerts.append(gate_name)

    db.session.commit()

    return jsonify({
        "status": "success",
        "new_alerts": new_alerts,
        "count": len(new_alerts),
    })


@alerts_bp.route("/api/alerts/resolve/<int:alert_id>", methods=["POST"])
def resolve_alert(alert_id):
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({"error": "Alert not found"}), 404
    alert.resolved = True
    db.session.commit()
    return jsonify({"status": "resolved", "alert_id": alert_id})


@alerts_bp.route("/api/alerts/clear-all", methods=["POST"])
def clear_all():
    Alert.query.filter_by(resolved=False).update({"resolved": True})
    db.session.commit()
    return jsonify({"status": "all alerts resolved"})
