import sys
import os
import json
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestAI(unittest.TestCase):
    def setUp(self):
        from ai.llm_engine import LLMEngine
        from ai.rag_engine import RAGEngine
        from ai.decision_engine import DecisionEngine
        self.llm = LLMEngine()
        self.rag = RAGEngine()
        self.decision = DecisionEngine()

    def test_intent_classification_navigation(self):
        intent = self.llm.classify_intent("Where is my seat B204?")
        self.assertEqual(intent, "navigation")

    def test_intent_classification_medical(self):
        intent = self.llm.classify_intent("I need a doctor, I am injured")
        self.assertEqual(intent, "medical")

    def test_intent_classification_food(self):
        intent = self.llm.classify_intent("I am hungry, where can I get food?")
        self.assertEqual(intent, "food")

    def test_intent_classification_emergency(self):
        intent = self.llm.classify_intent("Emergency! There is a fire")
        self.assertEqual(intent, "emergency")

    def test_intent_classification_transport(self):
        intent = self.llm.classify_intent("Is there a shuttle bus to the parking lot?")
        self.assertEqual(intent, "transport")

    def test_intent_classification_accessibility(self):
        intent = self.llm.classify_intent("Do you have wheelchair accessible routes?")
        self.assertEqual(intent, "accessibility")

    def test_language_detection_english(self):
        lang = self.llm.detect_language("Where is my seat?")
        self.assertEqual(lang, "en")

    def test_language_detection_spanish(self):
        lang = self.llm.detect_language("Necesito ayuda médica")
        self.assertEqual(lang, "es")

    def test_language_detection_hindi(self):
        lang = self.llm.detect_language("मुझे मदद चाहिए")
        self.assertEqual(lang, "hi")

    def test_language_detection_french(self):
        lang = self.llm.detect_language("Bonjour, où sont les toilettes?")
        self.assertEqual(lang, "fr")

    def test_rag_retrieve_context_navigation(self):
        context = self.rag.retrieve_context("I am at Gate A")
        self.assertIn("stadium", context)
        self.assertIn("name", context["stadium"])

    def test_rag_retrieve_context_medical(self):
        context = self.rag.retrieve_context("I need medical help")
        self.assertIn("relevant_zones", context)
        has_medical = any(z.get("type") == "medical" for z in context["relevant_zones"])
        self.assertTrue(has_medical)

    def test_rag_retrieve_context_emergency(self):
        context = self.rag.retrieve_context("Emergency evacuation")
        has_emergency = any(z.get("type") == "emergency" for z in context["relevant_zones"])
        self.assertTrue(has_emergency)

    def test_crowd_analysis_normal(self):
        result = self.decision.analyze_crowd({
            "gates": [
                {"gate": "A", "density": 30, "status": "normal"},
                {"gate": "B", "density": 25, "status": "normal"},
            ]
        })
        self.assertEqual(result["risk_level"], "low")

    def test_crowd_analysis_critical(self):
        result = self.decision.analyze_crowd({
            "gates": [
                {"gate": "A", "density": 95, "status": "critical"},
            ]
        })
        self.assertEqual(result["risk_level"], "high")
        self.assertIn("A", result["critical_gates"])
        self.assertGreater(len(result["recommendations"]), 0)

    def test_crowd_analysis_warning(self):
        result = self.decision.analyze_crowd({
            "gates": [
                {"gate": "C", "density": 65, "status": "warning"},
            ]
        })
        self.assertEqual(result["risk_level"], "medium")

    def test_generate_alert_critical(self):
        alert = self.decision.generate_alert({
            "gate": "B", "density": 90, "queue_time": 20, "status": "critical"
        })
        self.assertEqual(alert["severity"], "critical")
        self.assertIn("B", alert["gate"])
        self.assertGreater(len(alert["recommendations"]), 0)

    def test_generate_alert_normal(self):
        alert = self.decision.generate_alert({
            "gate": "A", "density": 20, "queue_time": 5, "status": "normal"
        })
        self.assertEqual(alert["severity"], "info")

    def test_fallback_general_response(self):
        response = self.llm._fallback_generate("", "Hello", "en")
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 10)

    def test_fallback_navigation_response(self):
        response = self.llm._fallback_generate("", "I am at Gate A where is seat B204?", "en")
        self.assertIn("Gate", response)

    def test_fallback_medical_response(self):
        response = self.llm._fallback_generate("", "I need medical help", "en")
        self.assertIn("Medical", response)

    def test_fallback_spanish_response(self):
        response = self.llm._fallback_generate("", "Necesito ayuda medica", "es")
        self.assertIn("asistencia", response.lower())

    def test_rag_crowd_summary(self):
        summary = self.rag.get_crowd_summary()
        self.assertIsNotNone(summary)

    def test_rag_nearest_medical(self):
        result = self.rag.find_nearest_medical("gate b")
        self.assertIsNotNone(result)

    def test_rag_find_nearest_exit(self):
        result = self.rag.find_nearest_exit("gate a")
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
