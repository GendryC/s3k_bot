import sqlite3

def get_all_cobros():
    with sqlite3.connect('clients.db') as conn:
        return [row[0] for row in conn.execute("SELECT date FROM cobro ORDER BY date DESC")]

def get_currency():
    with sqlite3.connect('clients.db') as conn:
        result = conn.execute("SELECT amount FROM currency LIMIT 1").fetchone()
        return result[0] if result else 1.0

def get_locations(status):
    with sqlite3.connect('clients.db') as conn:
        return conn.execute(
            "SELECT u.id, c.nombre, u.direccion, u.activa FROM ubicacion u JOIN ciudad c ON u.ciudad = c.id WHERE u.activa = ?",
            (status,)
        ).fetchall()

def delete_location(location_id):
    with sqlite3.connect('clients.db') as conn:
        conn.execute("DELETE FROM ubicacion WHERE id = ?", (location_id,))

def toggle_location(location_id):
    with sqlite3.connect('clients.db') as conn:
        conn.execute("UPDATE ubicacion SET activa = ? WHERE id = ?", (
            1 if conn.execute("SELECT activa FROM ubicacion WHERE id = ?", (location_id,)).fetchone()[0] == 0 else 0, location_id))
def save_data(date, clients):
    with sqlite3.connect('clients.db') as conn:
        conn.execute("INSERT OR REPLACE INTO clients (date, clients) VALUES (?, ?)", (date, clients))

def get_day_data(date):
    with sqlite3.connect('clients.db') as conn:
        result = conn.execute("SELECT clients FROM clients WHERE date = ?", (date,)).fetchone()
        return result[0] if result else 0

def add_city(nombre):
    with sqlite3.connect('clients.db') as conn:
        conn.execute("INSERT OR IGNORE INTO ciudad (nombre) VALUES (?)", (nombre,))

def get_cities():
    with sqlite3.connect('clients.db') as conn:
        return conn.execute("SELECT id, nombre FROM ciudad").fetchall()

def add_location(ciudad_id, direccion):
    with sqlite3.connect('clients.db') as conn:
        conn.execute("INSERT INTO ubicacion (ciudad, direccion, activa) VALUES (?, ?, 1)", (ciudad_id, direccion))