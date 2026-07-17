# ArenaShield AI

**GenAI-Powered Smart Stadium Operations & Fan Experience Platform**

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Tests](https://img.shields.io/badge/tests-86%20total-brightgreen)
![OpenRouter](https://img.shields.io/badge/AI-OpenRouter%20%7C%20OpenAI%20%7C%20Gemini%20%7C%20Groq-orange)
![Flask](https://img.shields.io/badge/framework-Flask-092E20)
![License](https://img.shields.io/badge/license-MIT-green)
![FIFA](https://img.shields.io/badge/FIFA%202026-Aligned-purple)

ArenaShield AI is a GenAI-powered platform that transforms stadium operations through intelligent fan assistance, real-time operational intelligence, and sustainable venue management.

---

## Problem Statement

Modern stadiums face critical challenges during large events:
- **Fan navigation** — Attendees struggle to locate seats, facilities, and emergency exits in large venues
- **Crowd congestion** — Poor gate distribution creates unsafe crowd pressure
- **Emergency response** — Staff need faster, data-driven decision support
- **Communication barriers** — International events require multilingual assistance
- **Operational blindspots** — Teams need real-time intelligence during live events
- **Sustainability goals** — FIFA 2026 requires green operations and waste management

---

## Solution

ArenaShield AI addresses these challenges with seven core components:

### 1. Fan AI Chat Concierge
Natural language stadium assistant with 774 searchable stadiums worldwide. Provides real-time seat navigation, medical emergency response with nearest facility locator, multilingual support (English, Spanish, Hindi, French), quick-action buttons, and voice input support via Web Speech API. Works with or without an AI provider using a built-in rule-based fallback engine.

### 2. Operations AI Copilot Dashboard
A professional command center with live gate monitoring (density, queue times, crowd flow with color-coded status), AI-generated alerts and recommendations, transport status tracking (shuttle buses, parking lots), and auto-refresh capability. Automatically syncs with the stadium selected in the Fan Assistant.

### 3. AI Incident Commander
Intelligent incident assessment system that analyzes gate density, medical requests, and security alerts in real-time. Assigns priority levels (LOW/MEDIUM/HIGH/CRITICAL) and generates actionable commands for staff deployment, crowd redirection, and resource allocation.

### 4. Green Operations AI
Sustainability monitoring module aligned with FIFA 2026 environmental goals. Tracks energy optimization (72-96%), water consumption efficiency, waste bin fill levels across all gates, carbon footprint, and provides AI-generated eco-suggestions.

### 5. Live Stadium Simulator
Three data generators that model real-time stadium conditions:
- **CrowdGenerator** — Realistic gate density and queue time variations
- **TransportGenerator** — Shuttle bus fleet and parking lot occupancy simulation
- **IncidentGenerator** — Medical, security, and maintenance event simulation
All data persists to `live_sensor.json` for real-time dashboard reflection.

### 6. Hybrid RAG Knowledge System
Context-aware retrieval system combining:
- **Vector Search** — N-gram based semantic similarity search across 774 stadiums
- **Keyword Retrieval** — Intent-based zone matching (medical, food, emergency)
- **Dynamic Layout Generation** — Per-stadium gate/block/amenity generation using seeded randomization
- **Emergency Procedures** — Structured response protocols

### 7. Dynamic Stadium Layout Engine
Every stadium now has complete gate, block, medical, food, washroom, and emergency exit data. Uses `stadiums.json` metadata combined with `stadium.json` template to generate unique layouts for all 774 stadiums via deterministic randomization.

---

## Features Overview

- Fan AI chat with intent classification, language detection, and prompt injection protection
- Voice input support (Web Speech API — no backend cost)
- Stadium selector with search and real-time filtering (774 stadiums worldwide)
- Dynamic stadium layout generation (gates, blocks, amenities for every stadium)
- Live gate monitoring with normal/warning/critical status indicators
- AI Incident Commander with priority assessment and automated commands
- AI Copilot with risk assessment and numbered recommendations
- Green Operations AI — energy, water, waste, carbon tracking
- Active alert management with resolve/clear actions
- Transport status tracking (shuttle buses, parking lots)
- SOS emergency button with contact numbers
- Rate limiting, security headers, input sanitization, and prompt injection mitigation
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
| Vector Search | N-gram semantic similarity (built-in, zero dependencies) |
| Frontend | HTML5, CSS3, Vanilla JavaScript (Web Speech API) |
| Security | Flask-Limiter, Flask-CORS, CSP Headers, Prompt Injection Guard |
| Testing | Python unittest + pytest (86 tests) |

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
| Fan Assistant | http://localhost:5000/ | AI Concierge chat + voice input + stadium selector |
| Operations Dashboard | http://localhost:5000/dashboard | Command center with AI Incident Commander + Green Ops |
| Health Check | http://localhost:5000/health | API health status |
| Debug | http://localhost:5000/debug | AI provider connectivity check |

---

## Project Structure

```
ArenaShield-AI/
├── app.py                  # Flask application factory + entry point
├── config.py               # Environment-based configuration
├── requirements.txt        # Python dependencies
├── .env.example            # API key template
├── ai/                     # GenAI Core
│   ├── llm_engine.py       # Multi-provider LLM + rule-based fallback + prompt injection protection
│   ├── rag_engine.py       # Hybrid RAG (vector search + keyword + layout generation)
│   ├── vector_store.py     # N-gram semantic search engine (zero dependencies)
│   ├── layout_generator.py # Dynamic stadium layout generator for 774 stadiums
│   ├── decision_engine.py  # Crowd analysis & alert generation
│   ├── incident_commander.py # AI Incident Commander (priority + commands)
│   ├── sustainability.py   # Green Operations AI (energy, water, waste)
│   └── prompts.py          # System prompts + safety guardrails
├── routes/                 # Flask Blueprints
│   ├── chat.py             # Fan AI Concierge endpoints
│   ├── dashboard.py        # Operations dashboard endpoints
│   └── alerts.py           # Alert management endpoints
├── database/
│   ├── models.py           # ChatHistory, Alert, SensorReading
│   └── database.py         # DB init helper
├── data/                   # Knowledge base
│   ├── stadiums.json       # 774 global stadiums
│   ├── stadium.json        # Detailed stadium layout template
│   ├── emergency.json      # Emergency procedures
│   └── live_sensor.json    # Real-time sensor data
├── simulator/
│   ├── crowd_generator.py      # Gate density simulation
│   ├── transport_generator.py  # Parking & shuttle simulation
│   └── incident_generator.py   # Medical/security events
├── templates/              # fan.html (with voice input), dashboard.html (with IC + sustainability)
├── static/                 # style.css (design system), script.js (app logic + voice)
├── tests/                  # 86 tests: AI, API, security, RAG, simulator
│   ├── test_ai.py          # 25 AI engine tests
│   ├── test_api.py         # 19 API endpoint tests
│   ├── test_security.py    # 16 security tests (incl. prompt injection)
│   ├── test_rag.py         # 10 RAG + layout generation tests
│   └── test_simulator.py   # 12 simulator tests
└── instance/               # SQLite database (auto-created)
```

---

## API Endpoints

### Chat & Stadium
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stadiums` | List all 774 stadiums |
| POST | `/api/stadium/select` | Select active stadium |
| GET | `/api/stadium/context` | Get current stadium info with layout |
| POST | `/api/chat` | Send message to AI assistant |
| GET | `/api/chat/history` | Get chat history by session_id |
| POST | `/api/intent` | Detect intent/language without response |

### Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/overview` | Stadium overview stats + live data |
| GET | `/api/dashboard/gates` | Live gate monitoring with alerts |
| GET | `/api/dashboard/ai-analysis` | AI crowd analysis & recommendations |
| GET | `/api/dashboard/incident-commander` | AI Incident Commander assessment |
| GET | `/api/dashboard/sustainability` | Green Operations AI status |
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
# Run all 86 tests
python -m pytest tests/ -v

# Run specific test suites
python -m pytest tests/test_ai.py -v          # AI engine (25 tests)
python -m pytest tests/test_api.py -v         # API endpoints (19 tests)
python -m pytest tests/test_security.py -v    # Security (16 tests)
python -m pytest tests/test_rag.py -v         # RAG + layout (10 tests)
python -m pytest tests/test_simulator.py -v   # Simulator (12 tests)
```

**Test coverage:**
- **AI Engine** — Intent classification, language detection, fallback responses, crowd analysis, alert generation
- **API Endpoints** — All chat, stadium, dashboard, alerts, incident commander, and sustainability endpoints
- **Security** — XSS injection, SQL injection, malformed JSON, rate limiting (200/min), security headers (CSP, HSTS, X-Frame-Options), CORS, PII leakage, **prompt injection** (ignore instructions, jailbreak attempts)
- **RAG** — Vector store search, context retrieval for medical/food/navigation, dynamic layout generation, layout fallback
- **Simulator** — Crowd, transport, and incident generator structure, field validation, range validation

> **Note:** API tests that call the live AI provider may take 15-30 seconds each. Run with `-k "not chat"` to skip slow AI-dependent tests.

---

## Security Features

- **Prompt Injection Mitigation** — Pattern-based detection of jailbreak attempts, ignore-instruction attacks, API key extraction, and DAN-style prompts
- **Input Sanitization** — All user messages HTML-escaped before rendering
- **Rate Limiting** — 200 requests/minute per IP
- **Security Headers** — CSP, HSTS, X-Frame-Options, X-Content-Type-Options, X-XSS-Protection
- **SQL Injection Protection** — SQLAlchemy parameterized queries
- **CORS** — Cross-Origin Resource Sharing enabled
- **PII Protection** — System does not echo personal data from messages

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `TypeError: Client.__init__() got an unexpected keyword argument 'proxies'` | openai SDK version incompatible with httpx | `pip install --upgrade openai` |
| Chat returns rule-based responses only | API key missing or provider unavailable | Check `/debug` endpoint, verify API key in `.env` |
| "AI Service Error" in chat | Network error or invalid API key | Verify API key is valid and has credits |
| Voice input not working | Browser doesn't support Web Speech API | Use Chrome/Edge, or type manually |
| Stadium selector shows no results | Server not running or network issue | Check `http://localhost:5000/health` |

---

## License

MIT
