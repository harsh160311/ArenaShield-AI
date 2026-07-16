# ArenaShield AI

**GenAI-Powered Smart Stadium Operations & Fan Experience Platform**

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
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
- Stadium selector with search and real-time filtering (700+ stadiums)
- Live gate monitoring with normal/warning/critical status indicators
- AI Copilot with risk assessment and numbered recommendations
- Active alert management with resolve actions
- Transport status tracking (shuttle buses, parking lots)
- SOS emergency button with contact numbers
- Rate limiting, security headers, and input sanitization
- Fully responsive design (mobile, tablet, desktop)
- Multilingual support (English, Spanish, Hindi, French)
- Rule-based fallback — fully functional without API keys

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python Flask 3.0 |
| Database | SQLite via SQLAlchemy |
| AI Providers | OpenRouter, OpenAI GPT-4, Gemini Pro, Groq Llama3 |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Security | Flask-Limiter, Flask-CORS, CSP Headers |

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
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env         # Configure your AI provider
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

| Page | URL |
|------|-----|
| Fan Assistant | http://localhost:5000/ |
| Operations Dashboard | http://localhost:5000/dashboard |
| Health Check | http://localhost:5000/health |

---

## Project Structure

```
ArenaShield-AI/
├── app.py              # Flask application
├── config.py           # Configuration
├── requirements.txt
├── .env.example
├── ai/                 # GenAI Core (LLM, RAG, decision engine, prompts)
├── routes/             # Flask Blueprints (chat, dashboard, alerts)
├── database/           # SQLAlchemy models
├── data/               # Knowledge base (stadiums, emergency, sensors)
├── simulator/          # Crowd, transport, incident generators
├── templates/          # fan.html, dashboard.html
├── static/             # style.css, script.js
└── tests/              # AI, API, and security tests
```

---

## API Endpoints

### Chat & Stadium
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stadiums` | List all stadiums |
| POST | `/api/stadium/select` | Select active stadium |
| POST | `/api/chat` | Send message to AI assistant |
| GET | `/api/chat/history` | Get chat history |

### Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/overview` | Stadium overview stats |
| GET | `/api/dashboard/gates` | Live gate monitoring |
| GET | `/api/dashboard/ai-analysis` | AI crowd analysis |
| POST | `/api/dashboard/refresh` | Trigger simulator |

### Alerts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/alerts` | Get active alerts |
| POST | `/api/alerts/generate` | Auto-generate alerts |
| POST | `/api/alerts/resolve/<id>` | Resolve an alert |

---

## Testing

```bash
python -m pytest tests/
```

Covers AI engine validation, API endpoint testing, and security testing (XSS, SQLi, rate limiting, headers).

---

## License

MIT
