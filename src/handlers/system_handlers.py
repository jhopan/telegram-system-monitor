"""
System Handlers
"""
from telegram import Update
from telegram.ext import ContextTypes
from src.utils.decorators import require_admin
from src.utils.helpers import send_long_message
from src.modules.system import (
    get_system_info,
    get_cpu_info,
    get_memory_info,
    get_uptime,
    get_processes_info,
    get_users_info
)


@require_admin
async def system_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /system"""
    info = get_system_info()
    await send_long_message(update, info)


@require_admin
async def cpu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /cpu"""
    info = get_cpu_info()
    await send_long_message(update, info)


@require_admin
async def memory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /memory"""
    info = get_memory_info()
    await send_long_message(update, info)


@require_admin
async def uptime_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /uptime"""
    info = get_uptime()
    await update.message.reply_text(info, parse_mode='Markdown')


@require_admin
async def processes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /processes"""
    info = get_processes_info()
    await send_long_message(update, info)


@require_admin
async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /users"""
    info = get_users_info()
    await update.message.reply_text(info, parse_mode='Markdown')
