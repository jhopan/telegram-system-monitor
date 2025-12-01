"""
Device Handlers
"""
from telegram import Update
from telegram.ext import ContextTypes
from src.utils.decorators import require_admin
from src.utils.helpers import send_long_message
from src.modules.device import (
    get_device_info,
    get_sensors_info,
    get_battery_info
)


@require_admin
async def device_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /device"""
    info = get_device_info()
    await send_long_message(update, info)


@require_admin
async def sensors_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /sensors"""
    info = get_sensors_info()
    await send_long_message(update, info)


@require_admin
async def battery_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /battery"""
    info = get_battery_info()
    await update.message.reply_text(info, parse_mode='Markdown')
