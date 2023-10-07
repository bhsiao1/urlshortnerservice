import sqlite3

# connect to database
conn = sqlite3.connect('urls.db')
cursor = conn.cursor()

# create the URLS table if doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        long_url TEXT NOT NULL,
        short_code TEXT NOT NULL UNIQUE
    )
''')

# commit changes, close connection
conn.commit()
conn.close()

print("Database initialized successfully.")