import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestRAG(unittest.TestCase):
    def setUp(self):
        from ai.rag_engine import RAGEngine
        self.rag = RAGEngine()

    def test_vector_store_search(self):
        self.rag.vector_store._build_index()
        results = self.rag.vector_store.search("Wembley", top_k=3)
        self.assertGreater(len(results), 0)
        self.assertIn("score", results[0])

    def test_vector_store_empty_query(self):
        results = self.rag.vector_store.search("", top_k=3)
        self.assertIsInstance(results, list)

    def test_vector_store_no_match(self):
        results = self.rag.vector_store.search("xyznonexistentxxxx", top_k=3)
        self.assertIsInstance(results, list)

    def test_context_retrieval_navigation(self):
        ctx = self.rag.retrieve_context("I am at Gate A")
        self.assertIn("stadium", ctx)
        self.assertIn("layout", ctx)

    def test_context_retrieval_medical(self):
        ctx = self.rag.retrieve_context("I need a doctor")
        has_medical = any(z.get("type") == "medical" for z in ctx.get("relevant_zones", []))
        self.assertTrue(has_medical)

    def test_context_retrieval_food(self):
        ctx = self.rag.retrieve_context("Where can I eat?")
        has_food = any(z.get("type") == "food" for z in ctx.get("relevant_zones", []))
        self.assertTrue(has_food)

    def test_layout_generation(self):
        from ai.layout_generator import generate_stadium_layout
        layout = generate_stadium_layout("wembley")
        self.assertIn("gates", layout)
        self.assertGreater(len(layout["gates"]), 0)
        self.assertIn("seating_blocks", layout)
        self.assertIn("medical_rooms", layout)
        self.assertIn("food_zones", layout)

    def test_layout_generation_fallback(self):
        from ai.layout_generator import generate_stadium_layout
        layout = generate_stadium_layout("nonexistent-id-12345")
        self.assertIn("gates", layout)
        self.assertGreater(len(layout["gates"]), 0)

    def test_stadium_context_with_layout(self):
        ctx = self.rag.get_stadium_context()
        self.assertIn("gates", ctx)
        self.assertIn("blocks", ctx)
        self.assertIn("medical", ctx)
        self.assertIn("food", ctx)


if __name__ == "__main__":
    unittest.main()
