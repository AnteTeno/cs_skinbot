from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

@app.get("/api/deals")
def get_deals():
    df = Analyzer.get_dataframe()
    deals = Analyzer.find_deals(df)
    return deals.to_dict(orient="records")

@app.post("/api/signup")
def signup(user: User):
    if Authenticator.signup(user.username, user.email, user.password):
        return {"message": "User created successfully"}
    else:
        raise HTTPException(status_code=400, detail="Username or email already exists")

@app.post("/api/login")
def login(user: User):
    token = Authenticator.login(user.username, user.password)
    if token:
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
