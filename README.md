# ArenaShield AI

**GenAI-Powered Smart Stadium Operations & Fan Experience Platform**

![Status](https://img.shields.io/badge/status-hackathon--ready-success)
![Flask](https://img.shields.io/badge/framework-Flask-092E20)
![Python](https://img.shields.io/badge/language-Python-3776AB)
![GenAI](https://img.shields.io/badge/powered%20by-GenAI-FF6F00)
![OpenRouter](https://img.shields.io/badge/ai-OpenRouter-FF6600)

---

## Problem Statement

Modern stadiums face critical challenges during large events:

- **Fan navigation challenges**: Attendees often struggle to locate seats, facilities, and emergency exits in large venues.
- **Crowd congestion**: Poor gate distribution can create unsafe crowd pressure.
- **Emergency response**: Staff need faster, data-driven decision support.
- **Communication barriers**: International events require multilingual assistance.
- **Operational blindspots**: Teams need real-time intelligence during live events.

---

## Solution

ArenaShield AI is a lightweight, GenAI-powered platform that transforms stadium operations through:

- **Fan AI Concierge**: Intelligent chat assistant providing personalized navigation, medical assistance, multilingual support, and real-time guidance
- **Operations AI Copilot**: Professional dashboard with live gate monitoring, AI-generated alerts, crowd analysis, and actionable recommendations
- **Smart Simulator**: Realistic data generation engine that models crowd behavior, transport status, and incidents
- **RAG Knowledge System**: Context-aware retrieval system combining stadium layout, emergency procedures, and live sensor data

---

## GenAI Architecture

```
User Query
    │
    ▼
┌─────────────────────────┐
│  Intent Classification  │ ← LLM / Rule-based hybrid classification
│  Language Detection     │    (navigation, medical, emergency, etc.)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Context Retrieval      │ ← RAG Engine
│  (RAG Engine)           │    queries stadium.json, stadiums.json,
│                         │    emergency.json, live_sensor.json
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  RAG Pipeline           │
│  ┌───────────────────┐  │
│  │ Context Extraction │  │ ← Parse user query for gates, zones, intent
│  │ Keyword Retrieval  │  │ ← Match against stadium & emergency KB
│  │ Knowledge Filtering│  │ ← Filter by zone, language, relevance
│  │ Prompt Augmentation│  │ ← Inject context into system prompt
│  └───────────────────┘  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  LLM (AI Provider)      │ ← OpenRouter / OpenAI / Gemini / Groq
│  (OpenRouter preferred) │    Falls back to rule-based engine
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  AI Response            │ ← Navigation / Medical / Emergency
│  + Recommendations      │    guidance with structured data
└─────────────────────────┘
```

---

## Why Generative AI?

ArenaShield AI does not use AI only for conversation.

GenAI is used for:

- Understanding natural language queries
- Generating personalized navigation guidance
- Summarizing operational incidents
- Creating crowd management recommendations
- Generating multilingual emergency responses
- Providing context-aware decisions using RAG

---

## Features

### 1. Fan AI Chat Concierge
- Natural language stadium assistant with 700+ searchable stadiums worldwide
- Real-time seat navigation with crowd-aware routing across configurable stadium zones
- Medical emergency response with nearest facility locator
- Multilingual support (English, Spanish, Hindi, French) — auto-detected or manually selected
- 4 quick-action buttons (Medical, Find Seat, Food, Emergency)
- Live stadium information sidebar with gate density, SOS button, and tips
- Rule-based fallback when no AI provider is configured

### 2. Stadium Selector
- Full-screen modal overlay with search and real-time filtering
- Search by stadium name, location, or country with grouped results
- Close button (X), click-outside-to-close, Escape key support
- Selected stadium persists via sessionStorage
- "Use default stadium" option for instant start

### 3. Operations AI Copilot Dashboard
- Automatically displays the same stadium selected in the Fan Assistant — no separate setup needed
- **Overview Stats**: Total visitors, average density, active alerts, medical requests, transport status with stadium name/location
- **Live Gate Monitoring**: Real-time density, queue times, crowd flow with color-coded status (normal/warning/critical)
- **AI Copilot Box**: Risk level assessment, situation summary, AI-generated numbered recommendations
- **Active Alerts**: Auto-generated alerts for critical/warning gate conditions with resolve action
- **Transport Status**: Shuttle bus availability, parking lot occupancy percentages
- Auto-refresh toggle and manual refresh with simulator trigger

### 4. Live Stadium Simulator
- `CrowdGenerator`: Realistic gate density and queue time variations with status thresholds
- `TransportGenerator`: Shuttle bus fleet simulation (active/en-route/waiting) and parking lot occupancy
- `IncidentGenerator`: Medical, security, and maintenance event simulation with weighted randomness
- All generators persist to `live_sensor.json` for real-time dashboard reflection

### 5. RAG Knowledge System
- `stadium.json`: Simulated stadium infrastructure model containing gates, seating blocks, medical rooms, food courts, washrooms, emergency exits, accessibility info
- `stadiums.json`: 700+ searchable global stadium database with names, locations, countries, and capacities
- `emergency.json`: Fire, medical, security, and weather procedures with contacts and medical centers
- Context-aware retrieval that identifies relevant zones based on user intent

The RAG pipeline performs:
- Context extraction from user query
- Keyword-based retrieval across stadium and emergency knowledge bases
- Relevant knowledge filtering by zone and intent
- Prompt augmentation with retrieved context
- LLM response generation grounded in retrieved stadium and operational context

### 6. Security & Accessibility
- Rate limiting (200 req/min)
- Security headers (CSP, HSTS, XSS protection, X-Frame-Options)
- Input validation and sanitization (2000 char limit)
- ARIA labels, keyboard navigation, focus-visible outlines
- Fully responsive design (mobile, tablet, desktop)
- Prominent SOS Emergency button with modal and contact numbers

---

## Design System

The UI follows a professional stadium technology theme using the 60-30-10 color rule:

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| **60% — Dominant** | Off White | `#F7F5EF` | Backgrounds, content areas, cards |
| **30% — Primary** | Stadium Green | `#0B3D2E` | Navigation, headers, buttons, headings |
| **10% — Accent** | Championship Gold | `#D4AF37` | Icons, highlights, active states, borders |
| **Semantic** | Green / Orange / Red | `#2E7D32` / `#F57C00` / `#C62828` | Status indicators, alerts |

- **Typography**: Inter (Google Fonts) with system fallbacks
- **Icons**: Font Awesome 6 via CDN
- **Theming**: CSS custom properties for consistent theming across all components
- **Aesthetic**: Clean, enterprise-ready — avoids cyberpunk/neon in favor of accessibility and clarity

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python Flask 3.0 |
| **Database** | SQLite via SQLAlchemy |
| **AI Providers** | OpenRouter / OpenAI GPT-4 / Gemini Pro / Groq Llama3 |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Security** | Flask-Limiter, Flask-CORS, CSP Headers |
| **Typography** | Inter (Google Fonts) |
| **Icons** | Font Awesome 6 |

---

## Installation

### Prerequisites
- Python 3.9+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/ArenaShield-AI.git
cd ArenaShield-AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your AI provider API key
```

### AI Provider Configuration

The application works out of the box with a rule-based fallback engine. For GenAI-powered responses, configure one provider:

**Option 1: OpenRouter (Recommended — 200+ models via single API key)**
```env
AI_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-your-api-key
```

**Option 2: Groq (Free tier available)**
```env
AI_PROVIDER=groq
GROQ_API_KEY=gsk_your_api_key
```

**Option 3: OpenAI**
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key
```

**Option 4: Google Gemini**
```env
AI_PROVIDER=gemini
GEMINI_API_KEY=your-api-key
```

---

## Running

```bash
python app.py
```

The application will be available at:
- **Fan Assistant**: http://localhost:5000/
- **Operations Dashboard**: http://localhost:5000/dashboard
- **Health Check**: http://localhost:5000/health

### Demo Walkthrough

1. Open the Fan Assistant at `http://localhost:5000/`
2. Search for a stadium or click "Use default stadium"
3. Type "I am at Gate A and my seat is B204" — AI provides navigation
4. Type "Necesito ayuda médica" — AI responds in Spanish with medical center info
5. Click "Emergency" quick button — Emergency guidance
6. Open Dashboard at `http://localhost:5000/dashboard`
7. Click "Refresh Data" to trigger simulator updates
8. Watch AI Copilot analyze crowd patterns and generate recommendations

---

## Project Structure

```
ArenaShield-AI/
│
├── app.py                  # Flask application factory, security headers, routes
├── config.py               # Configuration from .env (AI providers, DB, secrets)
├── requirements.txt        # Python dependencies
├── README.md               # Documentation
├── .env.example           # Environment template
│
├── ai/                     # GenAI Core
│   ├── __init__.py
│   ├── llm_engine.py       # LLM abstraction (OpenAI/Gemini/Groq/OpenRouter + rule-based fallback)
│   ├── rag_engine.py       # Retrieval Augmented Generation engine
│   ├── decision_engine.py  # AI crowd analysis & alert generation
│   └── prompts.py          # System prompts & templates for all intents
│
├── routes/                 # Flask Blueprints
│   ├── __init__.py
│   ├── chat.py             # Fan chat API endpoints + stadium selection
│   ├── dashboard.py        # Operations dashboard API
│   └── alerts.py           # Alert management API
│
├── database/               # Data Layer
│   ├── __init__.py
│   ├── database.py         # Database initialization helper
│   └── models.py           # SQLAlchemy models (ChatHistory, Alert, SensorReading)
│
├── data/                   # Knowledge Base
│   ├── stadium.json        # Simulated stadium layout with gates, blocks, amenities
│   ├── stadiums.json       # 700+ searchable global stadium database
│   ├── emergency.json      # Emergency procedures, contacts, medical centers
│   └── live_sensor.json    # Live simulated sensor readings
│
├── simulator/              # Data Generators
│   ├── __init__.py
│   ├── crowd_generator.py  # Gate crowd density simulation with variance
│   ├── transport_generator.py  # Shuttle bus & parking lot simulation
│   └── incident_generator.py   # Medical/security/maintenance event simulation
│
├── templates/              # Frontend Templates
│   ├── fan.html           # Fan AI Chat interface (search-first, stadium selector)
│   └── dashboard.html     # Operations command center dashboard
│
├── static/                 # Static Assets
│   ├── style.css          # Complete design system (responsive, 60-30-10 theme)
│   └── script.js          # Frontend application logic (chat, search, dashboard)
│
└── tests/                  # Automated Tests
    ├── __init__.py
    ├── test_ai.py          # AI engine tests (intent, language, RAG, decisions)
    ├── test_api.py         # API endpoint tests (all routes, status codes)
    └── test_security.py    # Security tests (XSS, SQLi, rate limiting, headers)
```

---

## API Endpoints

### Chat & Stadium
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stadiums` | List all available stadiums |
| POST | `/api/stadium/select` | Select active stadium by ID |
| GET | `/api/stadium/context` | Get current stadium info |
| POST | `/api/chat` | Send message to AI assistant |
| GET | `/api/chat/history` | Get chat history by session |
| POST | `/api/intent` | Detect message intent |

### Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/overview` | Stadium overview statistics |
| GET | `/api/dashboard/gates` | Live gate monitoring data |
| GET | `/api/dashboard/ai-analysis` | AI crowd analysis & recommendations |
| POST | `/api/dashboard/refresh` | Trigger all simulators |
| GET | `/api/dashboard/sensor-history` | Historical sensor readings |

### Alerts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/alerts` | Get active alerts |
| POST | `/api/alerts/generate` | Auto-generate alerts from sensor data |
| POST | `/api/alerts/resolve/<id>` | Resolve a specific alert |
| POST | `/api/alerts/clear-all` | Clear all active alerts |

---

## Database Models

| Table | Key Fields | Purpose |
|-------|-----------|---------|
| `ChatHistory` | session_id, role, message, language, timestamp | Persists fan chat conversations |
| `Alert` | gate, alert_type, severity, message, ai_recommendations, resolved | Tracks operational alerts |
| `SensorReading` | gate, density, queue_time, crowd_flow, status, timestamp | Historical sensor data |

---

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test suites
python tests/test_ai.py
python tests/test_api.py
python tests/test_security.py

# Run with coverage
pip install pytest-cov
python -m pytest tests/ --cov=. --cov-report=html
```

### Test Coverage

- **AI engine validation**: Intent classification, language detection, RAG retrieval, crowd analysis, alert generation, fallback responses
- **API endpoint testing**: All API endpoints, status codes, response validation, error handling
- **Input security testing**: XSS prevention, SQL injection, rate limiting, security headers, input validation, CORS, method validation

---

## Security Considerations

- **Environment-based API key management**: Keys stored in `.env`, never hardcoded
- **Input sanitization before AI processing**: Message length limits (2000 chars), JSON validation, empty body rejection
- **Rate limiting against abuse**: 200 requests per minute per client via Flask-Limiter
- **Secure HTTP headers on every response**:
  - Content-Security-Policy (restricts scripts/styles to self + CDN)
  - X-Content-Type-Options (nosniff)
  - X-Frame-Options (DENY)
  - X-XSS-Protection (1; mode=block)
  - Strict-Transport-Security (production HTTPS deployment)
- **No sensitive user information storage**: Chat history stored without PII; no user accounts
- **Prompt injection mitigation**: Controlled system prompts with clear role boundaries
- **SQL injection prevention**: SQLAlchemy ORM with parameterized queries

---

## Hackathon Alignment

ArenaShield AI addresses the challenge requirements by combining:

- GenAI-powered fan assistance
- Crowd-aware navigation
- Operational intelligence
- Multilingual accessibility
- Real-time decision support

---

## Key Differentiators

- ✅ Fully functional with or without API keys (rule-based fallback engine)
- ✅ OpenRouter support — access 200+ AI models via single API key
- ✅ 700+ searchable stadiums worldwide with real-time filtering
- ✅ Search-first UI with integrated navbar, stadium selector overlay, and keyboard navigation
- ✅ Fully responsive design (mobile, tablet, desktop) with CSS custom properties
- ✅ Professional 60-30-10 design system (Off White / Stadium Green / Championship Gold)
- ✅ Under 10 MB repository size — no node_modules or heavy frameworks
- ✅ Comprehensive test suite covering AI, API, and security
- ✅ GenAI integration with multi-stage RAG pipeline
- ✅ Real-time simulation for live demonstrations
- ✅ Multilingual support (English, Spanish, Hindi, French)

---

## Impact

ArenaShield AI transforms a traditional stadium into an intelligent environment where fans receive personalized assistance and operators receive AI-powered recommendations for safer, faster, and smarter event management.

---

## License

MIT License — see LICENSE file for details.
