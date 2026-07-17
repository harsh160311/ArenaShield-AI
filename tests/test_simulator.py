import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestSimulator(unittest.TestCase):
    def setUp(self):
        from simulator.crowd_generator import CrowdGenerator
        from simulator.transport_generator import TransportGenerator
        from simulator.incident_generator import IncidentGenerator
        self.crowd = CrowdGenerator()
        self.transport = TransportGenerator()
        self.incident = IncidentGenerator()

    def test_crowd_generator_structure(self):
        data = self.crowd.generate()
        self.assertIn("gates", data)
        self.assertIn("total_visitors", data)
        self.assertGreater(len(data["gates"]), 0)

    def test_crowd_gate_fields(self):
        data = self.crowd.generate()
        for gate in data["gates"]:
            self.assertIn("gate", gate)
            self.assertIn("density", gate)
            self.assertIn("queue_time", gate)
            self.assertIn("crowd_flow", gate)
            self.assertIn("status", gate)

    def test_crowd_density_range(self):
        data = self.crowd.generate()
        for gate in data["gates"]:
            self.assertGreaterEqual(gate["density"], 0)
            self.assertLessEqual(gate["density"], 100)

    def test_crowd_queue_time_positive(self):
        data = self.crowd.generate()
        for gate in data["gates"]:
            self.assertGreaterEqual(gate["queue_time"], 0)

    def test_transport_generator_structure(self):
        data = self.transport.generate()
        self.assertIn("shuttle_buses", data)
        self.assertIn("parking", data)

    def test_transport_shuttle_fields(self):
        data = self.transport.generate()
        shuttle = data["shuttle_buses"]
        self.assertIn("operational", shuttle)
        self.assertIn("en_route", shuttle)
        self.assertIn("waiting", shuttle)

    def test_transport_parking_structure(self):
        data = self.transport.generate()
        self.assertGreater(len(data["parking"]), 0)

    def test_incident_generator_structure(self):
        data = self.incident.generate()
        self.assertIn("active_medical", data)
        self.assertIn("security_alerts", data)
        self.assertIn("maintenance_requests", data)

    def test_incident_ranges(self):
        data = self.incident.generate()
        self.assertGreaterEqual(data["active_medical"], 0)
        self.assertGreaterEqual(data["security_alerts"], 0)
        self.assertGreaterEqual(data["maintenance_requests"], 0)

    def test_incident_timestamp(self):
        data = self.incident.generate()
        self.assertIn("generated_at", data)


if __name__ == "__main__":
    unittest.main()
