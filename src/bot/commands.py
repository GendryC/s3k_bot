import sqlite3
import calendar
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from tabulate import tabulate

from bot.db import (
    get_all_cobros, get_currency, get_locations, save_data, get_day_data,
    add_city, get_cities, add_location, delete_location, toggle_location
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["/insert", "/facturar"],
        ["/week", "/month"],
        ["/ubicaciones_act", "/ubicaciones_inact"],
        ["/ubicacion_toggle", "/ciudad_add", "/ciudades"],
        ["/ubicacion_add", "/ubicacion_del"],
        ["/cobro", "/cancelar_cobro" , "/currency"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Selecciona una opción:", reply_markup=reply_markup)

async def week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now()
    start = today - timedelta(days=today.weekday())
    total = 0
    rows = []
    for i in range(7):
        d = (start + timedelta(days=i)).strftime("%Y-%m-%d")
        count = get_day_data(d)
        rows.append([d, count])
        total += count
    table = tabulate(rows, headers=["Día", "Clientes"], tablefmt="github")
    await update.message.reply_text(f"Clientes esta semana:\n{table}\nTotal: {total}")

async def month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now()
    _, last_day = calendar.monthrange(today.year, today.month)
    weeks = []
    week = []
    total = 0
    for d in range(1, last_day + 1):
        date = f"{today.year}-{today.month:02d}-{d:02d}"
        count = get_day_data(date)
        week.append(count)
        if len(week) == 7 or d == last_day:
            weeks.append(week)
            week = []
        total += count
    msg = "Clientes por semana del mes:\n"
    for idx, w in enumerate(weeks):
        msg += f"Semana {idx+1}: {w} (Total: {sum(w)})\n"
    msg += f"Total del mes: {total}"
    await update.message.reply_text(msg)

async def facturar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cobros = get_all_cobros()
    if not cobros:
        await update.message.reply_text("No hay días de cobro")
        return
    msg = "Cobros anteriores:\n"
    for c in cobros:
        msg += f"- {c}\n"
    last = cobros[0]
    total = 0
    start = datetime.strptime(last, "%Y-%m-%d") + timedelta(days=1)
    today = datetime.now()
    d = start
    while d <= today:
        count = get_day_data(d.strftime("%Y-%m-%d"))
        total += count
        d += timedelta(days=1)
    currency = get_currency()
    msg += f"\n{total} clientes desde {start.date()} a {today.date()} = ${total * currency:.2f}"
    await update.message.reply_text(msg)

async def currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(context.args[0])
        if amount <= 0:
            await update.message.reply_text("El monto debe ser positivo")
            return
        with sqlite3.connect('clients.db') as conn:
            conn.execute("DELETE FROM currency")
            conn.execute("INSERT INTO currency (amount) VALUES (?)", (amount,))
        await update.message.reply_text(f"Monto por cliente: ${amount}")
    except:
        await update.message.reply_text("Uso: /currency <monto>")

async def ubicacion_del(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        location_id = int(context.args[0])
        delete_location(location_id)
        await update.message.reply_text(f"Ubicación {location_id} eliminada.")
    except:
        await update.message.reply_text("Error al eliminar ubicación. Usa /ubicacion_del <id>")

async def ubicacion_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        location_id = int(context.args[0])
        # activa = int(context.args[1])
        # if activa not in (0, 1):
        #     await update.message.reply_text("Valor debe ser 1 o 0")
        #     return
        toggle_location(location_id)
        await update.message.reply_text(f"Ubicación {location_id} toggled.")
    except:
        await update.message.reply_text("Error. Usa /ubicacion_toggle <id> <1|0>")

def format_ubicaciones_por_ciudad(locs):
    if not locs:
        return None
    ciudades = {}
    for loc in locs:
        loc_id, ciudad, direccion, *rest = loc
        if ciudad not in ciudades:
            ciudades[ciudad] = []
        ciudades[ciudad].append((loc_id, direccion))
    msg = ""
    for ciudad, ubicaciones in ciudades.items():
        msg += f"{ciudad}:\n"
        for loc_id, direccion in ubicaciones:
            msg += f"    - id {loc_id} | {direccion}\n"
    return msg

async def ubicaciones_activas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    locs = get_locations(1)
    msg = format_ubicaciones_por_ciudad(locs)
    if not msg:
        await update.message.reply_text("No hay ubicaciones activas.")
        return
    await update.message.reply_text(f"Ubicaciones activas:\n{msg}")

async def ubicaciones_inactivas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    locs = get_locations(0)
    msg = format_ubicaciones_por_ciudad(locs)
    if not msg:
        await update.message.reply_text("No hay ubicaciones inactivas.")
        return
    await update.message.reply_text(f"Ubicaciones inactivas:\n{msg}")

#  Comando para agregar ciudad
async def ciudad_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        nombre = " ".join(context.args)
        if not nombre:
            await update.message.reply_text("Uso: /ciudad_add <nombre>")
            return
        add_city(nombre)
        await update.message.reply_text(f"Ciudad '{nombre}' agregada.")
    except Exception as e:
        await update.message.reply_text(f"Error al agregar ciudad: {e}")

# --- Comando para listar ciudades ---
async def ciudades(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cities = get_cities()
    if not cities:
        await update.message.reply_text("No hay ciudades registradas.")
        return
    msg = "Ciudades registradas:\n"
    for cid, nombre in cities:
        msg += f"{cid}: {nombre}\n"
    await update.message.reply_text(msg)

# --- Comando para agregar ubicación ---
async def ubicacion_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 2:
            await update.message.reply_text("Uso: /ubicacion_add <ciudad_id> <dirección>")
            return
        ciudad_id = int(context.args[0])
        direccion = " ".join(context.args[1:])
        add_location(ciudad_id, direccion)
        await update.message.reply_text(f"Ubicación agregada en ciudad {ciudad_id}: {direccion}")
    except Exception as e:
        await update.message.reply_text(f"Error al agregar ubicación: {e}")

# --- Comando para guardar clientes de un día ---
async def insert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 2:
            await update.message.reply_text("Uso: /insert <YYYY-MM-DD> <cantidad>")
            return
        date = context.args[0]
        clients = int(context.args[1])
        save_data(date, clients)
        await update.message.reply_text(f"Guardados {clients} clientes para {date}")
    except Exception as e:
        await update.message.reply_text(f"Error al guardar datos: {e}")