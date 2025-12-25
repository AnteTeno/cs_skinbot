# CS Skinbot

A CS:GO skin trading bot that analyzes market data to identify profitable trading opportunities.

## Features

- **Market Analysis** — Fetches 500+ item listings from CSGOEmpire API and identifies profitable trades
- **User Authentication** — Secure JWT-based auth with password hashing
- **Data Storage** — SQLite database storing 1000+ market records for trend analysis
- **Web Interface** — React dashboard for monitoring deals

## Tech Stack

| Backend | Frontend |
|---------|----------|
| Python / FastAPI | React |
| SQLite | JavaScript |
| JWT Authentication | CSS |

## Project Structure
```
cs_skinbot/
├── backend/
│   ├── main.py          # API routes
│   ├── Analyzer.py      # Market analysis logic
│   ├── Fetcher.py       # CSGOEmpire API integration
│   ├── Authenticator.py # JWT auth & password hashing
│   └── Database.py      # SQLite operations
└── frontend/
    └── src/
        ├── App.js
        └── components/   # Login, Signup, Dashboard
```

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
```

Create `.env`:
```
CSGO_EMPIRE_API_KEY=your_api_key
SECRET_KEY=your_jwt_secret
```

Run:
```bash
uvicorn main:app --reload
```

API docs: `http://localhost:8000/docs`

### Frontend
```bash
cd frontend
npm install
npm start
```

App runs on `http://localhost:3000`

## License

MIT
