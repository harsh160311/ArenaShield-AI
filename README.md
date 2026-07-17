# ArenaShield AI

**GenAI-Powered Smart Stadium Operations & Fan Experience Platform**

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Tests](https://img.shields.io/badge/tests-58%20total-brightgreen)
![OpenRouter](https://img.shields.io/badge/AI-OpenRouter%20%7C%20OpenAI%20%7C%20Gemini%20%7C%20Groq-orange)
![Flask](https://img.shields.io/badge/framework-Flask-092E20)
![License](https://img.shields.io/badge/license-MIT-green)

ArenaShield AI is a GenAI-powered platform that transforms stadium operations through intelligent fan assistance and real-time operational intelligence.

---

## Problem Statement

Modern stadiums face critical challenges during large events:
- **Fan navigation** — Attendees struggle to locate seats, facilities, and emergency exits in large venues
- **Crowd congestion** — Poor gate distribution creates unsafe crowd pressure
- **Emergency response** — Staff need faster, data-driven decision support
- **Communication barriers** — International events require multilingual assistance
- **Operational blindspots** — Teams need real-time intelligence during live events

---

## Solution

ArenaShield AI addresses these challenges with four core components:

### 1. Fan AI Chat Concierge
Natural language stadium assistant with 700+ searchable stadiums worldwide. Provides real-time seat navigation, medical emergency response with nearest facility locator, multilingual support (English, Spanish, Hindi, French), and quick-action buttons for Medical, Find Seat, Food, and Emergency. Works with or without an AI provider using a built-in rule-based fallback engine.

### 2. Operations AI Copilot Dashboard
A professional command center with live gate monitoring (density, queue times, crowd flow with color-coded status), AI-generated alerts and recommendations, transport status tracking (shuttle buses, parking lots), and auto-refresh capability. Automatically syncs with the stadium selected in the Fan Assistant.

### 3. Live Stadium Simulator
Three data generators that model real-time stadium conditions:
- **CrowdGenerator** — Realistic gate density and queue time variations
- **TransportGenerator** — Shuttle bus fleet and parking lot occupancy simulation
- **IncidentGenerator** — Medical, security, and maintenance event simulation
All data persists to `live_sensor.json` for real-time dashboard reflection.

### 4. RAG Knowledge System
Context-aware retrieval system combining stadium infrastructure data, 700+ global stadium database, emergency procedures, and live sensor data. The pipeline performs context extraction, keyword retrieval, knowledge filtering, and prompt augmentation to ground AI responses in accurate stadium and operational context.

---

## Features Overview

- Fan AI chat with intent classification and language detection
- Stadium selector with search and real-time filtering (774 stadiums worldwide)
- Live gate monitoring with normal/warning/critical status indicators
- AI Copilot with risk assessment and numbered recommendations
- Active alert management with resolve/clear actions
- Transport status tracking (shuttle buses, parking lots)
- SOS emergency button with contact numbers
- Rate limiting, security headers, and input sanitization
- Fully responsive design (mobile, tablet, desktop)
- Multilingual support (English, Spanish, Hindi, French)
- Rule-based fallback — fully functional without API keys
- Real-time data simulator for crowd, transport, and incidents
- Sensor reading history with time-series data
- Debug endpoint for API connectivity verification

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python Flask 3.0 |
| Database | SQLite via SQLAlchemy |
| AI Providers | OpenRouter, OpenAI GPT-4o, Gemini Pro, Groq Llama3 |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Security | Flask-Limiter, Flask-CORS, CSP Headers |
| Testing | Python unittest + pytest |

---

## Quick Start

### Prerequisites
- Python 3.9+
- pip

### Setup

```bash
git clone https://github.com/harsh160311/ArenaShield-AI.git
cd ArenaShield-AI
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate
pip install -r requirements.txt
# Copy and configure your AI provider:
cp .env.example .env
# Edit .env and set your API key
python app.py
```

> **Note:** If you encounter `TypeError: Client.__init__() got an unexpected keyword argument 'proxies'`, upgrade openai: `pip install --upgrade openai`

### AI Provider Configuration

The app works out of the box with rule-based fallback. For GenAI responses, set one provider in `.env`:

**OpenRouter (Recommended)** — 200+ models via single API key
```
AI_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-your-key
```

**Groq** — Free tier available
```
AI_PROVIDER=groq
GROQ_API_KEY=gsk_your_key
```

**OpenAI** or **Google Gemini** also supported.

### Access the App

| Page | URL | Description |
|------|-----|-------------|
| Fan Assistant | http://localhost:5000/ | AI Concierge chat + stadium selector |
| Operations Dashboard | http://localhost:5000/dashboard | Command center with live monitoring |
| Health Check | http://localhost:5000/health | API health status |
| Debug | http://localhost:5000/debug | AI provider connectivity check |

---

## Project Structure

```
ArenaShield-AI/
├── app.py              # Flask application factory + entry point
├── config.py           # Environment-based configuration
├── requirements.txt    # Python dependencies
├── .env.example        # API key template
├── ai/                 # GenAI Core
│   ├── llm_engine.py   # Multi-provider LLM + rule-based fallback
│   ├── rag_engine.py   # Retrieval-Augmented Generation
│   ├── decision_engine.py  # Crowd analysis & alerts
│   └── prompts.py      # System prompts
├── routes/             # Flask Blueprints
│   ├── chat.py         # Fan AI Concierge endpoints
│   ├── dashboard.py    # Operations dashboard endpoints
│   └── alerts.py       # Alert management endpoints
├── database/
│   ├── models.py       # ChatHistory, Alert, SensorReading
│   └── database.py     # DB init helper
├── data/               # Knowledge base
│   ├── stadiums.json   # 774 global stadiums
│   ├── stadium.json    # Detailed stadium layout
│   ├── emergency.json  # Emergency procedures
│   └── live_sensor.json # Real-time sensor data
├── simulator/
│   ├── crowd_generator.py    # Gate density simulation
│   ├── transport_generator.py # Parking & shuttle simulation
│   └── incident_generator.py # Medical/security events
├── templates/          # fan.html, dashboard.html
├── static/             # style.css (design system), script.js (app logic)
├── tests/              # 58 tests: AI, API, and security
└── instance/           # SQLite database (auto-created)
```

---

## API Endpoints

### Chat & Stadium
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stadiums` | List all 774 stadiums |
| POST | `/api/stadium/select` | Select active stadium |
| GET | `/api/stadium/context` | Get current stadium info |
| POST | `/api/chat` | Send message to AI assistant |
| GET | `/api/chat/history` | Get chat history by session_id |
| POST | `/api/intent` | Detect intent/language without response |

### Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/overview` | Stadium overview stats + live data |
| GET | `/api/dashboard/gates` | Live gate monitoring with alerts |
| GET | `/api/dashboard/ai-analysis` | AI crowd analysis & recommendations |
| POST | `/api/dashboard/refresh` | Trigger all simulators |
| GET | `/api/dashboard/stadium` | Get dashboard stadium context |
| GET | `/api/dashboard/sensor-history` | Last 100 sensor readings |

### Alerts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/alerts` | Get unresolved alerts |
| POST | `/api/alerts/generate` | Auto-generate from sensor data |
| POST | `/api/alerts/resolve/<id>` | Resolve a specific alert |
| POST | `/api/alerts/clear-all` | Resolve all active alerts |

---

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test suites
python -m pytest tests/test_ai.py -v        # AI engine (25 tests)
python -m pytest tests/test_api.py -v       # API endpoints (19 tests)
python -m pytest tests/test_security.py -v  # Security (14 tests)
```

**Test coverage:**
- **AI Engine** — Intent classification, language detection, fallback responses, RAG context retrieval, crowd analysis, alert generation
- **API Endpoints** — All chat, stadium, dashboard, and alerts endpoints with valid/invalid inputs
- **Security** — XSS injection, SQL injection, malformed JSON, rate limiting (200/min), security headers (CSP, HSTS, X-Frame-Options), CORS, PII leakage

> **Note:** API tests that call the live AI provider may take 15-30 seconds each. Run with `-k "not chat"` to skip slow AI-dependent tests.

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `TypeError: Client.__init__() got an unexpected keyword argument 'proxies'` | openai SDK version incompatible with httpx | `pip install --upgrade openai` |
| Chat returns rule-based responses only | API key missing or provider unavailable | Check `/debug` endpoint, verify API key in `.env` |
| "AI Service Error" in chat | Network error or invalid API key | Verify API key is valid and has credits |
| Empty gates/blocks in stadium context | Stadium data only in `stadiums.json`, detailed layout in `stadium.json` | See Known Issues below |
| Stadium selector shows no results | Server not running or network issue | Check `http://localhost:5000/health` |

## Known Issues

- **Language detection false positive:** Spanish indicator `"el"` matches inside English word `"help"`, causing incorrect language detection. Being refactored to word-boundary matching.
- **Stadium layout data gap:** `stadiums.json` (774 stadiums) contains only basic metadata. Detailed layout data (gates, blocks, amenities) is only available in `stadium.json` and is not dynamically loaded per stadium. All non-default stadiums return empty gate/block arrays.
- **No custom 404 handler:** Unknown routes return Flask's default 404 HTML page instead of a JSON response.

## License

MIT
