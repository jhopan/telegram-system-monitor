"""
Network Handlers
"""
from telegram import Update
from telegram.ext import ContextTypes
from src.utils.decorators import require_admin
from src.utils.helpers import send_long_message
from src.modules.network import (
    get_network_info,
    get_network_stats,
    get_network_connections,
    get_public_ip,
    ping_host,
    get_routing_table,
    get_dns_info
)


@require_admin
async def network_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /network"""
    info = get_network_info()
    await send_long_message(update, info)


@require_admin
async def netstats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /netstats"""
    info = get_network_stats()
    await update.message.reply_text(info, parse_mode='Markdown')


@require_admin
async def connections_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /connections"""
    info = get_network_connections()
    await send_long_message(update, info)


@require_admin
async def publicip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /publicip"""
    info = get_public_ip()
    await update.message.reply_text(info, parse_mode='Markdown')


@require_admin
async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /ping <host>"""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/ping <host>`\nContoh: `/ping google.com`",
            parse_mode='Markdown'
        )
        return
    
    host = context.args[0]
    await update.message.reply_text(f"⏳ Pinging {host}...")
    info = ping_host(host)
    await update.message.reply_text(info, parse_mode='Markdown')


@require_admin
async def route_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /route"""
    info = get_routing_table()
    await update.message.reply_text(info, parse_mode='Markdown')


@require_admin
async def dns_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /dns"""
    info = get_dns_info()
    await update.message.reply_text(info, parse_mode='Markdown')
