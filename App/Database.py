import sqlite3
import hashlib

def connect():
    return sqlite3.connect('cs_skinbot.db')

def init_db():
    conn = connect()
    c = conn.cursor()
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)


    
    c.execute("""
    CREATE TABLE IF NOT EXISTS deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        deal_id INTEGER,
        amount REAL NOT NULL,
        transaction_type TEXT NOT NULL,  -- esim. 'buy' tai 'sell'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (deal_id) REFERENCES deals(id) ON DELETE SET NULL
    )
    """)
    conn.commit()
    conn.close()

def insert_user(username, email, password_hash):
    conn = sqlite3.connect("cs_skinbot.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                       (username, email, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  
    finally:
        conn.close()
