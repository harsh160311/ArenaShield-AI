import os
import re
from config import Config
from ai.prompts import SYSTEM_PROMPT, SYSTEM_PROMPT_SAFETY

PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|above|prior)",
    r"forget\s+(all\s+)?(instructions|rules|prompts)",
    r"you\s+are\s+(not\s+)?(an?\s+)?(ai|assistant|chatbot)",
    r"system\s+prompt",
    r"api[_\s]?key",
    r"show\s+(me\s+)?your\s+(prompt|instructions|source)",
    r"act\s+as\s+(a\s+)?(sudo|root|admin|superuser)",
    r"password|secret|token|credential",
    r"DAN|jailbreak|bypass",
]


def _has_word(text, word):
    return bool(re.search(r'\b' + re.escape(word) + r'\b', text.lower()))


def _is_injection_attempt(message):
    msg_lower = message.lower()
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, msg_lower):
            return True
    return False


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
        if _is_injection_attempt(user_prompt):
            return "I can only assist with stadium-related questions. How can I help you with your visit today?"

        combined_prompt = f"{SYSTEM_PROMPT}\n\n{SYSTEM_PROMPT_SAFETY}\n\n{system_prompt}"

        if self.is_available():
            return self._call_api(combined_prompt, user_prompt)
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
            "A": "Gate A \u2192 Main Concourse \u2192 Corridor 1 \u2192 Block",
            "B": "Gate B \u2192 Corridor 2 \u2192 Block",
            "C": "Gate C \u2192 West Concourse \u2192 Corridor 3 \u2192 Block",
            "D": "Gate D \u2192 East Concourse \u2192 Corridor 4 \u2192 Block",
        }

        route = routes.get(gate, "Gate \u2192 Main Concourse \u2192 Block")
        times = {"A": "4", "B": "3", "C": "5", "D": "4"}

        if language == "es":
            return (
                f"**Ubicaci\u00f3n Actual:** {from_location}\n\n"
                f"**Ruta Recomendada:**\n{route} {block}\n\n"
                f"**Tiempo Estimado:** {times.get(gate, '4')} minutos\n\n"
                f"**Estado de Multitud:** Bajo\n\n"
                f"**Consejo:** Siga las se\u00f1alizaciones azules hacia su bloque."
            )
        elif language == "hi":
            return (
                f"**\u0935\u0930\u094d\u0924\u092e\u093e\u0928 \u0938\u094d\u0925\u093e\u0928:** {from_location}\n\n"
                f"**\u0905\u0928\u0941\u0936\u0902\u0938\u093f\u0924 \u092e\u093e\u0930\u094d\u0917:**\n{route} {block}\n\n"
                f"**\u0905\u0928\u0941\u092e\u093e\u0928\u093f\u0924 \u0938\u092e\u092f:** {times.get(gate, '4')} \u092e\u093f\u0928\u091f\n\n"
                f"**\u092d\u0940\u0921\u093c \u0915\u0940 \u0938\u094d\u0925\u093f\u0924\u093f:** \u0915\u092e\n\n"
                f"**\u0938\u0941\u091d\u093e\u0935:** \u0905\u092a\u0928\u0947 \u092c\u094d\u0932\u0949\u0915 \u0915\u0940 \u0913\u0930 \u0928\u0940\u0932\u0947 \u0938\u0902\u0915\u0947\u0924\u094b\u0902 \u0915\u093e \u092a\u093e\u0932\u0928 \u0915\u0930\u0947\u0902\u0964"
            )
        elif language == "fr":
            return (
                f"**Position Actuelle:** {from_location}\n\n"
                f"**Itin\u00e9raire Recommand\u00e9:**\n{route} {block}\n\n"
                f"**Temps Estim\u00e9:** {times.get(gate, '4')} minutes\n\n"
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
                "**Se requiere asistencia m\u00e9dica.**\n\n"
                "**Centro M\u00e9dico m\u00e1s cercano:**\n"
                "East Block - Primeros Auxilios\n\n"
                "**Distancia:** 150 metros\n\n"
                "**Contacto de Emergencia:** +1-800-STADIUM-911\n\n"
                "**Instrucciones:** Dir\u00edjase al Centro M\u00e9dico del East Block. "
                "Personal de primeros auxilios tambi\u00e9n est\u00e1 disponible en todas las puertas."
            )
        elif language == "hi":
            return (
                "**\u091a\u093f\u0915\u093f\u0924\u094d\u0938\u093e \u0938\u0939\u093e\u092f\u0924\u093e \u0915\u0940 \u0906\u0935\u0936\u094d\u092f\u0915\u0924\u093e \u0939\u0948\u0964**\n\n"
                "**\u0928\u093f\u0915\u091f\u0924\u092e \u091a\u093f\u0915\u093f\u0924\u094d\u0938\u093e \u0915\u0947\u0902\u0926\u094d\u0930:**\n"
                "\u0908\u0938\u094d\u091f \u092c\u094d\u0932\u0949\u0915 - \u092a\u094d\u0930\u093e\u0925\u092e\u093f\u0915 \u091a\u093f\u0915\u093f\u0924\u094d\u0938\u093e\n\n"
                "**\u0926\u0942\u0930\u0940:** 150 \u092e\u0940\u091f\u0930\n\n"
                "**\u0906\u092a\u093e\u0924\u0915\u093e\u0932\u0940\u0928 \u0938\u0902\u092a\u0930\u094d\u0915:** +1-800-STADIUM-911\n\n"
                "**\u0928\u093f\u0930\u094d\u0926\u0947\u0936:** \u0915\u0943\u092a\u092f\u093e \u0908\u0938\u094d\u091f \u092c\u094d\u0932\u0949\u0915 \u091a\u093f\u0915\u093f\u0924\u094d\u0938\u093e \u0915\u0947\u0902\u0926\u094d\u0930 \u092a\u0930 \u091c\u093e\u090f\u0902\u0964 "
                "\u0938\u092d\u0940 \u0917\u0947\u091f\u094b\u0902 \u092a\u0930 \u092a\u094d\u0930\u093e\u0925\u092e\u093f\u0915 \u091a\u093f\u0915\u093f\u0924\u094d\u0938\u093e \u0915\u0930\u094d\u092e\u0940 \u0909\u092a\u0932\u092c\u094d\u0927 \u0939\u0948\u0902\u0964"
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
            "\u2022 Gate A - North Exit\n"
            "\u2022 Corridor 2 - East Exit\n\n"
            "**Emergency Contacts:**\n"
            "\u2022 Stadium Security: +1-800-STADIUM-911\n"
            "\u2022 Medical Emergency: Ext. 911\n"
            "\u2022 Fire Safety: Ext. 100\n\n"
            "Staff are being notified. Follow their instructions."
        )

    def _food_response(self, query, language):
        return (
            "**Food & Beverage Options:**\n\n"
            "**Central Plaza Food Court:**\n"
            "\u2022 Gourmet Burgers - Section C1\n"
            "\u2022 Pizza World - Section C2\n"
            "\u2022 Asian Wok - Section C3\n\n"
            "**Block Concessions:**\n"
            "\u2022 Block A: Hot Dogs & Nachos\n"
            "\u2022 Block B: Sandwiches & Salads\n"
            "\u2022 Block C: Mexican Grill\n"
            "\u2022 Block D: Ice Cream & Desserts\n\n"
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
            "\u2022 Route 1: Stadium \u2194 City Center (Every 10 min)\n"
            "\u2022 Route 2: Stadium \u2194 Parking Lots A-D (Every 5 min)\n\n"
            "**Parking:**\n"
            "\u2022 Lot A: 25% available (recommended)\n"
            "\u2022 Lot B: 85% full\n"
            "\u2022 Lot C: 60% full\n\n"
            "**Metro Station:** Stadium West (5 min walk)"
        )

    def _accessibility_response(self, query, language):
        return (
            "**Accessibility Services:**\n\n"
            "**Wheelchair-Accessible Routes:**\n"
            "\u2022 All gates have ramp access\n"
            "\u2022 Elevators at Block A, C, and Central Plaza\n"
            "\u2022 Accessible seating in all blocks\n\n"
            "**Special Assistance:**\n"
            "\u2022 Request wheelchair at any gate\n"
            "\u2022 Visual assistance available\n"
            "\u2022 Hearing assistance devices at Information Desk\n\n"
            "**Contact Accessibility Services:** Ext. 500"
        )

    def _washroom_response(self, query, language):
        return (
            "**Washroom Locations:**\n\n"
            "**Near Gates:**\n"
            "\u2022 Gate A: Left corridor, 20m\n"
            "\u2022 Gate B: Right corridor, 15m\n"
            "\u2022 Gate C: Behind concession stand\n"
            "\u2022 Gate D: Near entrance, 10m\n\n"
            "**Inside Blocks:**\n"
            "\u2022 Each block has facilities at both ends\n"
            "\u2022 Family washrooms at Block B and D\n"
            "\u2022 Accessible washrooms at all locations"
        )

    def _general_response(self, query, language):
        return (
            "Welcome to ArenaShield AI! I'm your stadium assistant. "
            "I can help you with:\n\n"
            "\U0001f4cd **Navigation** - Find your seat, gates, amenities\n"
            "\U0001f691 **Medical** - Locate medical centers and first aid\n"
            "\U0001f354 **Food** - Discover dining options\n"
            "\u267f **Accessibility** - Wheelchair routes and assistance\n"
            "\U0001f68c **Transport** - Parking, shuttles, and transit\n"
            "\U0001f4ca **Crowd Info** - Live density and wait times\n\n"
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
        if any(_has_word(message, w) for w in ["medical", "doctor", "hospital", "injury", "hurt", "ayuda", "m\u00e9dica", "health"]):
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
        spanish_indicators = ["hola", "ayuda", "gracias", "por favor", "d\u00f3nde", "qu\u00e9",
                              "los", "las", "necesito", "quiero", "m\u00e9dica",
                              "emergencia", "ba\u00f1o", "comida", "salida"]
        french_indicators = ["bonjour", "merci", "s'il vous pla\u00eet", "o\u00f9", "aide",
                             "urgence", "m\u00e9dical", "toilettes", "nourriture", "sortie"]
        hindi_indicators = ["\u0928\u092e\u0938\u094d\u0924\u0947", "\u092e\u0926\u0926", "\u0915\u0939\u093e\u0901", "\u0915\u094d\u092f\u093e", "\u091a\u093e\u0939\u093f\u090f",
                            "\u092c\u093e\u0925\u0930\u0942\u092e", "\u0916\u093e\u0928\u093e", "\u0926\u094d\u0935\u093e\u0930", "\u0938\u0940\u091f"]

        msg_lower = message.lower()

        has_devanagari = bool(re.search(r'[\u0900-\u097F]', message))
        if has_devanagari:
            return "hi"

        for indicator in french_indicators:
            if indicator in msg_lower:
                return "fr"

        for indicator in spanish_indicators:
            if indicator in msg_lower:
                return "es"

        return "en"
