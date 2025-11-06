import sqlite3
import hashlib
import config

def connect():
    return sqlite3.connect(config.DATABASE_URL)

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
    CREATE TABLE IF NOT EXISTS item_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        market_name TEXT NOT NULL,
        purchase_price REAL NOT NULL,
        market_value REAL NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def insert_item_history(df):
    conn = connect()
    df.to_sql('item_history', conn, if_exists='append', index=False)
    conn.close()

def insert_user(username, email, password_hash):
    conn = connect()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                       (username, email, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        return str(e)
    finally:
        conn.close()
