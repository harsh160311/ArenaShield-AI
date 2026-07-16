import sys
import os
import json
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestAPI(unittest.TestCase):
    def setUp(self):
        from app import create_app
        app = create_app()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "healthy")

    def test_index_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ArenaShield", response.data)

    def test_dashboard_endpoint(self):
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Operations", response.data)

    def test_chat_endpoint_no_message(self):
        response = self.client.post(
            "/api/chat",
            content_type="application/json",
            data=json.dumps({})
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_chat_endpoint_valid(self):
        response = self.client.post(
            "/api/chat",
            content_type="application/json",
            data=json.dumps({"message": "Where is my seat?"})
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("response", data)
        self.assertIn("session_id", data)
        self.assertIn("intent", data)

    def test_chat_endpoint_spanish(self):
        response = self.client.post(
            "/api/chat",
            content_type="application/json",
            data=json.dumps({"message": "Necesito ayuda médica", "language": "es"})
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["language"], "es")

    def test_chat_endpoint_long_message(self):
        response = self.client.post(
            "/api/chat",
            content_type="application/json",
            data=json.dumps({"message": "x" * 2500})
        )
        self.assertEqual(response.status_code, 400)

    def test_intent_endpoint(self):
        response = self.client.post(
            "/api/intent",
            content_type="application/json",
            data=json.dumps({"message": "I need a doctor"})
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["intent"], "medical")

    def test_dashboard_overview(self):
        response = self.client.get("/api/dashboard/overview")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("total_visitors", data)
        self.assertIn("gates", data)

    def test_dashboard_gates(self):
        response = self.client.get("/api/dashboard/gates")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("gates", data)

    def test_dashboard_ai_analysis(self):
        response = self.client.get("/api/dashboard/ai-analysis")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("risk_level", data)

    def test_dashboard_refresh(self):
        response = self.client.post("/api/dashboard/refresh")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")

    def test_alerts_endpoint(self):
        response = self.client.get("/api/alerts")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_alerts_generate(self):
        self.client.post("/api/dashboard/refresh")
        response = self.client.post("/api/alerts/generate")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")

    def test_chat_history_no_session(self):
        response = self.client.get("/api/chat/history")
        self.assertEqual(response.status_code, 400)

    def test_chat_history_valid(self):
        self.client.post(
            "/api/chat",
            content_type="application/json",
            data=json.dumps({"message": "Hello", "session_id": "test-session"})
        )
        response = self.client.get("/api/chat/history?session_id=test-session")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreater(len(data), 0)

    def test_resolve_alert_not_found(self):
        response = self.client.post("/api/alerts/resolve/99999")
        self.assertEqual(response.status_code, 404)

    def test_clear_alerts(self):
        response = self.client.post("/api/alerts/clear-all")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_sensor_history(self):
        response = self.client.get("/api/dashboard/sensor-history")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)


if __name__ == "__main__":
    unittest.main()
