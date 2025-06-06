import sqlite3

def init_db():
    conn = sqlite3.connect('clients.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clients (date TEXT PRIMARY KEY, clients INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS cobro (date TEXT PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS currency (amount REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS ciudad (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS ubicacion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ciudad INTEGER,
        direccion TEXT,
        activa INTEGER DEFAULT 1,
        FOREIGN KEY (ciudad) REFERENCES ciudad(id)
    )''')
    conn.commit()
    conn.close()