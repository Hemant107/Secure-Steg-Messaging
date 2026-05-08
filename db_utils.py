import sqlite3

DB = "stego.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        action TEXT,
        filename TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def add_history(username, action, filename):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO history (username, action, filename) VALUES (?, ?, ?)",
              (username, action, filename))
    conn.commit()
    conn.close()

def get_history(username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT action, filename, timestamp FROM history WHERE username=?", (username,))
    rows = c.fetchall()
    conn.close()
    return rows