"""
Disk Handlers
"""
from telegram import Update
from telegram.ext import ContextTypes
from src.utils.decorators import require_admin
from src.utils.helpers import send_long_message
from src.modules.disk import (
    get_disk_info,
    get_partitions_info,
    get_disk_io_stats
)


@require_admin
async def disk_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /disk"""
    info = get_disk_info()
    await send_long_message(update, info)


@require_admin
async def partitions_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /partitions"""
    info = get_partitions_info()
    await send_long_message(update, info)


@require_admin
async def diskio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /diskio"""
    info = get_disk_io_stats()
    await send_long_message(update, info)
