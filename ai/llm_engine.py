import os
import re
from config import Config


def _has_word(text, word):
    return bool(re.search(r'\b' + re.escape(word) + r'\b', text.lower()))


class LLMEngine:
    def __init__(self, provider=None):
        self.provider = provider or Config.AI_PROVIDER
        self.client = None
        self._init_client()

    def _init_client(self):
        if self.provider == "openai":
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            except Exception:
                self.client = None
        elif self.provider == "gemini":
            try:
                import google.generativeai as genai
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.client = genai.GenerativeModel(Config.GEMINI_MODEL)
            except Exception:
                self.client = None
        elif self.provider == "groq":
            try:
                from groq import Groq
                self.client = Groq(api_key=Config.GROQ_API_KEY)
            except Exception:
                self.client = None
        elif self.provider == "openrouter":
            try:
                from openai import OpenAI
                self.client = OpenAI(
                    api_key=Config.OPENROUTER_API_KEY,
                    base_url=Config.OPENROUTER_BASE_URL,
                )
            except Exception:
                self.client = None

    def is_available(self):
        if self.provider == "openai" and self.client:
            return bool(Config.OPENAI_API_KEY)
        elif self.provider == "gemini" and self.client:
            return bool(Config.GEMINI_API_KEY)
        elif self.provider == "groq" and self.client:
            return bool(Config.GROQ_API_KEY)
        elif self.provider == "openrouter" and self.client:
            return bool(Config.OPENROUTER_API_KEY)
        return False

    def generate(self, system_prompt, user_prompt, language="en"):
        if self.is_available():
            return self._call_api(system_prompt, user_prompt)
        return self._fallback_generate(system_prompt, user_prompt, language)

    def _call_api(self, system_prompt, user_prompt):
        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=Config.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.7,
                    max_tokens=512,
                )
                return response.choices[0].message.content

            elif self.provider == "gemini":
                full_prompt = f"{system_prompt}\n\n{user_prompt}"
                response = self.client.generate_content(full_prompt)
                return response.text

            elif self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=Config.GROQ_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.7,
                    max_tokens=512,
                )
                return response.choices[0].message.content

            elif self.provider == "openrouter":
                response = self.client.chat.completions.create(
                    model=Config.OPENROUTER_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.7,
                    max_tokens=1024,
                    extra_headers={
                        "HTTP-Referer": "https://arenashield.ai",
                        "X-Title": "ArenaShield AI",
                    }
                )
                return response.choices[0].message.content

        except Exception as e:
            return f"[AI Service Error: {str(e)}]"

        return "AI service unavailable. Please check your API configuration."

    def _fallback_generate(self, system_prompt, user_prompt, language="en"):
        return self._rule_based_response(user_prompt, language)

    def _rule_based_response(self, query, language="en"):
        query_lower = query.lower()

        if any(_has_word(query, w) for w in ["medical", "doctor", "hospital", "injury", "hurt", "ayuda", "médica"]):
            return self._medical_response(query_lower, language)

        if any(_has_word(query, w) for w in ["emergency", "fire", "evacuate", "help"]):
            return self._emergency_response(query_lower, language)

        if any(_has_word(query, w) for w in ["seat", "where", "find", "navigate", "location", "gate", "block"]):
            return self._navigation_response(query_lower, language)

        if any(_has_word(query, w) for w in ["food", "hungry", "restaurant", "concession", "comida"]):
            return self._food_response(query_lower, language)

        if any(_has_word(query, w) for w in ["crowd", "density", "busy", "crowded"]):
            return self._crowd_response(query_lower, language)

        if any(_has_word(query, w) for w in ["transport", "bus", "parking", "shuttle", "train"]):
            return self._transport_response(query_lower, language)

        if any(_has_word(query, w) for w in ["wheelchair", "accessible", "accessibility", "disability"]):
            return self._accessibility_response(query_lower, language)

        if any(_has_word(query, w) for w in ["washroom", "bathroom", "toilet", "restroom", "baño"]):
            return self._washroom_response(query_lower, language)

        return self._general_response(query, language)

    def _navigation_response(self, query, language):
        gate = "A"
        for g in ["a", "b", "c", "d"]:
            if f"gate {g}" in query:
                gate = g.upper()
                break

        block = "B2"
        for letter in "abcd":
            for num in range(1, 11):
                if f"{letter}{num}" in query or f"{letter.upper()}{num}" in query:
                    block = f"{letter.upper()}{num}"
                    break

        from_location = f"Gate {gate}"

        routes = {
            "A": "Gate A → Main Concourse → Corridor 1 → Block",
            "B": "Gate B → Corridor 2 → Block",
            "C": "Gate C → West Concourse → Corridor 3 → Block",
            "D": "Gate D → East Concourse → Corridor 4 → Block",
        }

        route = routes.get(gate, "Gate → Main Concourse → Block")
        times = {"A": "4", "B": "3", "C": "5", "D": "4"}

        if language == "es":
            return (
                f"**Ubicación Actual:** {from_location}\n\n"
                f"**Ruta Recomendada:**\n{route} {block}\n\n"
                f"**Tiempo Estimado:** {times.get(gate, '4')} minutos\n\n"
                f"**Estado de Multitud:** Bajo\n\n"
                f"**Consejo:** Siga las señalizaciones azules hacia su bloque."
            )
        elif language == "hi":
            return (
                f"**वर्तमान स्थान:** {from_location}\n\n"
                f"**अनुशंसित मार्ग:**\n{route} {block}\n\n"
                f"**अनुमानित समय:** {times.get(gate, '4')} मिनट\n\n"
                f"**भीड़ की स्थिति:** कम\n\n"
                f"**सुझाव:** अपने ब्लॉक की ओर नीले संकेतों का पालन करें।"
            )
        elif language == "fr":
            return (
                f"**Position Actuelle:** {from_location}\n\n"
                f"**Itinéraire Recommandé:**\n{route} {block}\n\n"
                f"**Temps Estimé:** {times.get(gate, '4')} minutes\n\n"
                f"**Affluence:** Faible\n\n"
                f"**Conseil:** Suivez les panneaux bleus vers votre bloc."
            )
        else:
            return (
                f"**Current Location:** {from_location}\n\n"
                f"**Recommended Route:**\n{route} {block}\n\n"
                f"**Estimated Time:** {times.get(gate, '4')} minutes\n\n"
                f"**Crowd Status:** Low\n\n"
                f"**Tip:** Follow the blue signage towards your block."
            )

    def _medical_response(self, query, language):
        if language == "es":
            return (
                "**Se requiere asistencia médica.**\n\n"
                "**Centro Médico más cercano:**\n"
                "East Block - Primeros Auxilios\n\n"
                "**Distancia:** 150 metros\n\n"
                "**Contacto de Emergencia:** +1-800-STADIUM-911\n\n"
                "**Instrucciones:** Diríjase al Centro Médico del East Block. "
                "Personal de primeros auxilios también está disponible en todas las puertas."
            )
        elif language == "hi":
            return (
                "**चिकित्सा सहायता की आवश्यकता है।**\n\n"
                "**निकटतम चिकित्सा केंद्र:**\n"
                "ईस्ट ब्लॉक - प्राथमिक चिकित्सा\n\n"
                "**दूरी:** 150 मीटर\n\n"
                "**आपातकालीन संपर्क:** +1-800-STADIUM-911\n\n"
                "**निर्देश:** कृपया ईस्ट ब्लॉक चिकित्सा केंद्र पर जाएं। "
                "सभी गेटों पर प्राथमिक चिकित्सा कर्मी उपलब्ध हैं।"
            )
        else:
            return (
                "**Medical assistance required.**\n\n"
                "**Nearest Medical Center:**\n"
                "East Block - First Aid Station\n\n"
                "**Distance:** 150 meters\n\n"
                "**Emergency Contact:** +1-800-STADIUM-911\n\n"
                "**Instructions:** Proceed to the East Block Medical Center. "
                "First aid staff are also available at all gate entrances."
            )

    def _emergency_response(self, query, language):
        return (
            "**EMERGENCY PROTOCOL ACTIVATED**\n\n"
            "**Immediate Steps:**\n"
            "1. Stay calm and assess your surroundings\n"
            "2. Follow the nearest emergency exit signs (green)\n"
            "3. Do NOT use elevators\n"
            "4. Proceed to the nearest assembly point\n\n"
            "**Nearest Emergency Exits:**\n"
            "• Gate A - North Exit\n"
            "• Corridor 2 - East Exit\n\n"
            "**Emergency Contacts:**\n"
            "• Stadium Security: +1-800-STADIUM-911\n"
            "• Medical Emergency: Ext. 911\n"
            "• Fire Safety: Ext. 100\n\n"
            "Staff are being notified. Follow their instructions."
        )

    def _food_response(self, query, language):
        return (
            "**Food & Beverage Options:**\n\n"
            "**Central Plaza Food Court:**\n"
            "• Gourmet Burgers - Section C1\n"
            "• Pizza World - Section C2\n"
            "• Asian Wok - Section C3\n\n"
            "**Block Concessions:**\n"
            "• Block A: Hot Dogs & Nachos\n"
            "• Block B: Sandwiches & Salads\n"
            "• Block C: Mexican Grill\n"
            "• Block D: Ice Cream & Desserts\n\n"
            "**Estimated Wait Time:** 5-8 minutes\n"
            "**Tip:** Use the ArenaShield app to pre-order and skip the line!"
        )

    def _crowd_response(self, query, language):
        return (
            "**Live Crowd Status:**\n\n"
            "**Gate A:** 45% density - Moderate\n"
            "**Gate B:** 90% density - HIGH CONGESTION\n"
            "**Gate C:** 30% density - Low\n"
            "**Gate D:** 55% density - Moderate\n\n"
            "**Recommendation:** Use Gate C for fastest entry. "
            "Gate B is experiencing heavy traffic."
        )

    def _transport_response(self, query, language):
        return (
            "**Transportation Options:**\n\n"
            "**Shuttle Buses:** Available at all gates\n"
            "• Route 1: Stadium ↔ City Center (Every 10 min)\n"
            "• Route 2: Stadium ↔ Parking Lots A-D (Every 5 min)\n\n"
            "**Parking:**\n"
            "• Lot A: 25% available (recommended)\n"
            "• Lot B: 85% full\n"
            "• Lot C: 60% full\n\n"
            "**Metro Station:** Stadium West (5 min walk)"
        )

    def _accessibility_response(self, query, language):
        return (
            "**Accessibility Services:**\n\n"
            "**Wheelchair-Accessible Routes:**\n"
            "• All gates have ramp access\n"
            "• Elevators at Block A, C, and Central Plaza\n"
            "• Accessible seating in all blocks\n\n"
            "**Special Assistance:**\n"
            "• Request wheelchair at any gate\n"
            "• Visual assistance available\n"
            "• Hearing assistance devices at Information Desk\n\n"
            "**Contact Accessibility Services:** Ext. 500"
        )

    def _washroom_response(self, query, language):
        return (
            "**Washroom Locations:**\n\n"
            "**Near Gates:**\n"
            "• Gate A: Left corridor, 20m\n"
            "• Gate B: Right corridor, 15m\n"
            "• Gate C: Behind concession stand\n"
            "• Gate D: Near entrance, 10m\n\n"
            "**Inside Blocks:**\n"
            "• Each block has facilities at both ends\n"
            "• Family washrooms at Block B and D\n"
            "• Accessible washrooms at all locations"
        )

    def _general_response(self, query, language):
        return (
            "Welcome to ArenaShield AI! I'm your stadium assistant. "
            "I can help you with:\n\n"
            "📍 **Navigation** - Find your seat, gates, amenities\n"
            "🚑 **Medical** - Locate medical centers and first aid\n"
            "🍔 **Food** - Discover dining options\n"
            "♿ **Accessibility** - Wheelchair routes and assistance\n"
            "🚌 **Transport** - Parking, shuttles, and transit\n"
            "📊 **Crowd Info** - Live density and wait times\n\n"
            "How can I help you today?"
        )

    def classify_intent(self, message):
        if self.is_available():
            from ai.prompts import INTENT_CLASSIFICATION_PROMPT
            prompt = INTENT_CLASSIFICATION_PROMPT.format(message=message)
            try:
                result = self._call_api("Classify the intent.", prompt)
                result = result.strip().lower()
                valid = ["navigation", "medical", "emergency", "food",
                         "accessibility", "transport", "information", "operations"]
                if result in valid:
                    return result
            except Exception:
                pass

        msg = message.lower()
        if any(_has_word(message, w) for w in ["medical", "doctor", "hospital", "injury", "hurt", "ayuda", "médica", "health"]):
            return "medical"
        if any(_has_word(message, w) for w in ["emergency", "fire", "evacuate", "help", "danger"]):
            return "emergency"
        if any(_has_word(message, w) for w in ["food", "hungry", "restaurant", "concession", "comida"]):
            return "food"
        if any(_has_word(message, w) for w in ["transport", "bus", "parking", "shuttle", "train", "metro"]):
            return "transport"
        if any(_has_word(message, w) for w in ["wheelchair", "accessible", "accessibility", "disability"]):
            return "accessibility"
        if any(_has_word(message, w) for w in ["where", "seat", "gate", "block", "find", "navigate", "route", "location"]):
            return "navigation"
        if any(_has_word(message, w) for w in ["crowd", "density", "busy", "congestion", "traffic"]):
            return "information"
        return "information"

    def detect_language(self, message):
        spanish_indicators = ["hola", "ayuda", "gracias", "por favor", "dónde", "qué",
                              "el", "la", "los", "las", "necesito", "quiero", "médica",
                              "emergencia", "baño", "comida", "salida"]
        french_indicators = ["bonjour", "merci", "s'il vous plaît", "où", "aide",
                             "urgence", "médical", "toilettes", "nourriture", "sortie"]
        hindi_indicators = ["नमस्ते", "मदद", "कहाँ", "क्या", "चाहिए", "बाथरूम",
                            "खाना", "द्वार", "सीट"]

        msg_lower = message.lower()
        for indicator in spanish_indicators:
            if indicator in msg_lower:
                return "es"
        for indicator in french_indicators:
            if indicator in msg_lower:
                return "fr"

        has_devanagari = bool(re.search(r'[\u0900-\u097F]', message))
        if has_devanagari:
            return "hi"

        return "en"
