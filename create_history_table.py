import sqlite3

# Step 1: Connect to database file (it will create if doesn't exist)
conn = sqlite3.connect('stego.db')  # yaha apna db file name use karo
c = conn.cursor()

# Step 2: Create table 'history' if not exists
c.execute('''
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    action TEXT NOT NULL,
    filename TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Step 3: Save changes and close connection
conn.commit()
conn.close()

print("History table created successfully!")
