from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import Analyzer
import Authenticator
import Database

app = FastAPI()

# CORS middleware
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    username: str
    email: str
    password: str

@app.on_event("startup")
def startup_event():
    Database.init_db()

@app.get("/api/market")
def get_market_data(authorization: Optional[str] = Header(None)):
    """Get all current market items with analysis (authentication optional but recommended)"""
    # Optional authentication - validate token if provided
    if authorization:
        try:
            token = authorization.replace("Bearer ", "")
            Authenticator.get_current_user(token)
        except:
            pass  # Continue without auth if token is invalid

    df = Analyzer.get_dataframe(pages=1)
    if df.empty:
        return {"items": [], "message": "No market data available"}

    # Return all items, sorted by discount percent (best deals first)
    df_sorted = df.sort_values('discount_percent', ascending=False)
    items = df_sorted.to_dict(orient="records")

    # Also try to find deals
    deals = Analyzer.find_deals(df)

    return {
        "items": items,
        "deal_count": len(deals),
        "total_items": len(df)
    }

@app.post("/api/signup")
def signup(user: User):
    result = Authenticator.signup(user.username, user.email, user.password)
    if result is True:
        return {"message": "User created successfully"}
    else:
        raise HTTPException(status_code=400, detail=result)

class LoginUser(BaseModel):
    username: str
    password: str

@app.post("/api/login")
def login(user: LoginUser):
    token = Authenticator.login(user.username, user.password)
    if token:
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
