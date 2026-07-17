import json
from ai.llm_engine import LLMEngine
from ai.prompts import INCIDENT_COMMANDER_PROMPT


class IncidentCommander:
    def __init__(self):
        self.llm = LLMEngine()

    def assess(self, sensor_data):
        gates = sensor_data.get("gates", [])
        incidents = sensor_data.get("incidents", {})
        transport = sensor_data.get("transport", {})

        critical = [g for g in gates if g.get("density", 0) >= 80 or g.get("status") == "critical"]
        warning = [g for g in gates if 50 <= g.get("density", 0) < 80 or g.get("status") == "warning"]
        active_medical = incidents.get("active_medical", 0)
        security = incidents.get("security_alerts", 0)

        priority = "LOW"
        if critical or active_medical > 2 or security > 0:
            priority = "CRITICAL"
        elif warning or active_medical > 0:
            priority = "HIGH"
        if priority == "LOW" and (critical or warning):
            priority = "MEDIUM"

        assessment = {
            "priority": priority,
            "situation": self._build_situation(critical, warning, active_medical, security),
            "critical_gates": [g.get("gate") for g in critical],
            "warning_gates": [g.get("gate") for g in warning],
            "active_medical": active_medical,
            "security_alerts": security,
        }

        if self.llm.is_available():
            try:
                prompt = INCIDENT_COMMANDER_PROMPT.format(
                    priority=priority,
                    situation=assessment["situation"],
                    gates=json.dumps(gates, indent=2),
                    incidents=json.dumps(incidents, indent=2),
                    transport=json.dumps(transport, indent=2),
                )
                ai_response = self.llm.generate(
                    "You are an AI Incident Commander for a stadium. Respond concisely.",
                    prompt,
                )
                assessment["ai_commands"] = ai_response
            except Exception:
                assessment["ai_commands"] = self._fallback_commands(priority, critical, warning)

        if not self.llm.is_available():
            assessment["ai_commands"] = self._fallback_commands(priority, critical, warning)

        return assessment

    def _build_situation(self, critical, warning, medical, security):
        parts = []
        if critical:
            gates_str = ", ".join([f"Gate {g.get('gate')} ({g.get('density')}%)" for g in critical])
            parts.append(f"Critical congestion at {gates_str}")
        if warning:
            gates_str = ", ".join([f"Gate {g.get('gate')} ({g.get('density')}%)" for g in warning])
            parts.append(f"Elevated density at {gates_str}")
        if medical:
            parts.append(f"{medical} active medical request(s)")
        if security:
            parts.append(f"{security} security alert(s)")
        if not parts:
            parts.append("All systems normal")
        return ". ".join(parts) + "."

    def _fallback_commands(self, priority, critical, warning):
        commands = []
        if priority == "CRITICAL":
            for g in critical:
                commands.append(f"Open additional entry points near Gate {g.get('gate')}")
                commands.append(f"Deploy 3 staff to Gate {g.get('gate')} immediately")
                commands.append(f"Activate digital signage redirecting from Gate {g.get('gate')}")
        elif priority == "HIGH":
            for g in warning:
                commands.append(f"Monitor Gate {g.get('gate')} closely")
                commands.append(f"Prepare backup staff for Gate {g.get('gate')}")
        commands.append("Notify command center of current status")
        commands.append(f"Priority: {priority}")
        return commands
