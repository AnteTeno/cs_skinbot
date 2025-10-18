from dotenv import load_dotenv
import os

load_dotenv()

CSGOEMPIRE_API_KEY = os.getenv("CSGOEMPIRE_API_KEY")

if not CSGOEMPIRE_API_KEY:
    raise ValueError("CSGOEMPIRE_API_KEY puuttuu .env-tiedostosta!")
