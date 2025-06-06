from bot.commands import *
from logger import get_logger
from telegram.ext import CommandHandler


def add_handlers(app):
    logger = get_logger()
    logger.info("Adding handlers")

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("week", week))
    app.add_handler(CommandHandler("month", month))
    app.add_handler(CommandHandler("facturar", facturar))
    app.add_handler(CommandHandler("currency", currency))
    app.add_handler(CommandHandler("ubicacion_del", ubicacion_del))
    app.add_handler(CommandHandler("ubicacion_toggle", ubicacion_toggle))
    app.add_handler(CommandHandler("ubicaciones_act", ubicaciones_activas))
    app.add_handler(CommandHandler("ubicaciones_inact", ubicaciones_inactivas))
    app.add_handler(CommandHandler("ciudad_add", ciudad_add))
    app.add_handler(CommandHandler("ciudades", ciudades))
    app.add_handler(CommandHandler("ubicacion_add", ubicacion_add))
    app.add_handler(CommandHandler("insert", insert))
    
    return app