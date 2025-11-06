## Project Overview

CS Skinbot is a Counter-Strike skin trading application that fetches deal data from CSGOEmpire API, analyzes market trends, and identifies profitable trading opportunities. The application consists of a FastAPI backend and a React frontend with user authentication.

## Project Structure

```
cs_skinbot/
├── backend/          # FastAPI backend
│   ├── main.py       # API routes and application entry point
│   ├── Analyzer.py   # Market analysis and deal-finding logic
│   ├── Fetcher.py    # CSGOEmpire API integration
│   ├── Authenticator.py  # JWT authentication and password hashing
│   ├── Database.py   # SQLite database operations
│   └── config.py     # Database configuration
└── frontend/         # React frontend
    └── src/
        ├── App.js           # Main routing component
        └── components/      # React components (Login, Signup, Dashboard)
```

## Development Setup

### Backend

**Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

**Required environment variables** (create `.env` in backend directory):
- `CSGO_EMPIRE_API_KEY` - API key for CSGOEmpire
- `SECRET_KEY` - JWT secret key for authentication

**Run the backend:**
```bash
cd backend
uvicorn main:app --reload
```

The FastAPI server will start on `http://localhost:8000`. API documentation is available at `http://localhost:8000/docs`.

### Frontend

**Install dependencies:**
```bash
cd frontend
npm install
```

**Run the frontend:**
```bash
cd frontend
npm start
```

The React app will start on `http://localhost:3000`.

**Run tests:**
```bash
cd frontend
npm test
```

**Build for production:**
```bash
cd frontend
npm run build
```