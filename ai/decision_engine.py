import json
import os
from ai.llm_engine import LLMEngine
from ai.prompts import CROWD_ANALYSIS_PROMPT


class DecisionEngine:
    def __init__(self):
        self.llm = LLMEngine()

    def analyze_crowd(self, sensor_data, alerts=None):
        if alerts is None:
            alerts = []

        analysis = self._rule_based_analysis(sensor_data, alerts)

        if self.llm.is_available():
            try:
                prompt = CROWD_ANALYSIS_PROMPT.format(
                    sensor_data=json.dumps(sensor_data, indent=2),
                    alerts=json.dumps(alerts, indent=2)
                )
                ai_analysis = self.llm.generate(
                    "You are a stadium operations AI. Analyze crowd data and provide recommendations.",
                    prompt
                )
                analysis["ai_analysis"] = ai_analysis
            except Exception:
                pass

        return analysis

    def _rule_based_analysis(self, sensor_data, alerts):
        critical_gates = []
        warning_gates = []
        recommendations = []
        risk_level = "low"

        gates_data = sensor_data.get("gates", sensor_data if isinstance(sensor_data, list) else [])

        if not gates_data:
            return {
                "risk_level": "unknown",
                "critical_gates": [],
                "warning_gates": [],
                "recommendations": ["No sensor data available."],
                "summary": "Insufficient data for analysis.",
            }

        for gate in gates_data:
            density = gate.get("density", 0)
            status = gate.get("status", "normal")
            gate_name = gate.get("gate", "Unknown")

            if density >= 80 or status == "critical":
                critical_gates.append(gate_name)
            elif density >= 50 or status == "warning":
                warning_gates.append(gate_name)

        if critical_gates:
            risk_level = "high"
            for gate in critical_gates:
                recommendations.append(f"Open additional entry points near {gate} to reduce congestion.")
                recommendations.append(f"Deploy 2-3 additional staff members to {gate} for crowd management.")
                recommendations.append(f"Update digital signage to redirect fans away from {gate}.")
                recommendations.append(f"Notify security team about critical density at {gate}.")
                recommendations.append(f"Consider temporary gate closure if density exceeds 95%.")
        elif warning_gates:
            risk_level = "medium"
            for gate in warning_gates:
                recommendations.append(f"Monitor {gate} closely - density is rising.")
                recommendations.append(f"Prepare backup staff for potential deployment to {gate}.")
        else:
            recommendations.append("All gates operating normally. Continue standard monitoring.")
            recommendations.append("Maintain current staffing levels.")

        recommendations.append("Send push notification to fans about current gate conditions.")

        summary_parts = []
        if critical_gates:
            summary_parts.append(f"⚠️ CRITICAL: High congestion at {', '.join(critical_gates)}.")
        if warning_gates:
            summary_parts.append(f"⚡ Warning: Elevated density at {', '.join(warning_gates)}.")
        if not critical_gates and not warning_gates:
            summary_parts.append("✅ All gates operating within normal parameters.")

        return {
            "risk_level": risk_level,
            "critical_gates": critical_gates,
            "warning_gates": warning_gates,
            "recommendations": recommendations[:7],
            "summary": " ".join(summary_parts),
        }

    def generate_alert(self, gate_data):
        density = gate_data.get("density", 0)
        gate_name = gate_data.get("gate", "Unknown")
        queue_time = gate_data.get("queue_time", 0)

        if density >= 80:
            severity = "critical"
            message = f"Critical congestion detected at {gate_name}. Density at {density}% with {queue_time}min queue time."
        elif density >= 50:
            severity = "warning"
            message = f"Moderate congestion at {gate_name}. Density at {density}%."
        else:
            severity = "info"
            message = f"Normal operations at {gate_name}. Density at {density}%."

        recommendations = self._rule_based_analysis(
            {"gates": [gate_data]}, []
        ).get("recommendations", [])

        return {
            "gate": gate_name,
            "severity": severity,
            "message": message,
            "recommendations": recommendations[:5],
        }
