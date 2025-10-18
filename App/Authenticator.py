import streamlit as st
import sqlite3
import hashlib


def verify_user(username, password):
    conn = sqlite3.connect("cs_skinbot.db")
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", 
                   (username, password_hash))
    user = cursor.fetchone()
    conn.close()
    
    return user is not None


