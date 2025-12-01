"""
Service Handlers
"""
from telegram import Update
from telegram.ext import ContextTypes
from src.utils.decorators import require_admin
from src.utils.helpers import send_long_message
from src.modules.service import (
    list_services,
    get_service_status,
    start_service,
    stop_service,
    restart_service,
    get_service_logs
)
from config.settings import config


@require_admin
async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /services"""
    filter_status = None
    if context.args:
        filter_status = context.args[0].lower()
        if filter_status not in ['running', 'failed', 'inactive']:
            filter_status = None
    
    info = list_services(filter_status)
    await send_long_message(update, info)


@require_admin
async def services_running_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /services_running"""
    info = list_services('running')
    await send_long_message(update, info)


@require_admin
async def services_failed_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /services_failed"""
    info = list_services('failed')
    await update.message.reply_text(info, parse_mode='Markdown')


@require_admin
async def service_status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /service_status <name>"""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/service_status <service_name>`\n"
            "Contoh: `/service_status nginx`",
            parse_mode='Markdown'
        )
        return
    
    service_name = context.args[0]
    info = get_service_status(service_name)
    await send_long_message(update, info)


@require_admin
async def service_logs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /service_logs <name> [lines]"""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/service_logs <service_name> [lines]`\n"
            "Contoh: `/service_logs nginx 100`",
            parse_mode='Markdown'
        )
        return
    
    service_name = context.args[0]
    lines = 50
    if len(context.args) > 1:
        try:
            lines = int(context.args[1])
        except:
            pass
    
    await update.message.reply_text("⏳ Mengambil logs...")
    info = get_service_logs(service_name, lines)
    await send_long_message(update, info)


@require_admin
async def service_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /service_start <name>"""
    if not config.ENABLE_SERVICE_CONTROL:
        await update.message.reply_text(
            "❌ Service control dinonaktifkan.\n"
            "Set ENABLE_SERVICE_CONTROL=true di .env",
            parse_mode='Markdown'
        )
        return
    
    if not context.args:
        await update.message.reply_text(
            "Usage: `/service_start <service_name>`\n"
            "Contoh: `/service_start nginx`\n\n"
            "⚠️ Bot harus dijalankan dengan sudo!",
            parse_mode='Markdown'
        )
        return
    
    service_name = context.args[0]
    info = start_service(service_name)
    await update.message.reply_text(info, parse_mode='Markdown')


@require_admin
async def service_stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /service_stop <name>"""
    if not config.ENABLE_SERVICE_CONTROL:
        await update.message.reply_text(
            "❌ Service control dinonaktifkan.\n"
            "Set ENABLE_SERVICE_CONTROL=true di .env",
            parse_mode='Markdown'
        )
        return
    
    if not context.args:
        await update.message.reply_text(
            "Usage: `/service_stop <service_name>`\n"
            "Contoh: `/service_stop nginx`\n\n"
            "⚠️ Bot harus dijalankan dengan sudo!",
            parse_mode='Markdown'
        )
        return
    
    service_name = context.args[0]
    info = stop_service(service_name)
    await update.message.reply_text(info, parse_mode='Markdown')


@require_admin
async def service_restart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /service_restart <name>"""
    if not config.ENABLE_SERVICE_CONTROL:
        await update.message.reply_text(
            "❌ Service control dinonaktifkan.\n"
            "Set ENABLE_SERVICE_CONTROL=true di .env",
            parse_mode='Markdown'
        )
        return
    
    if not context.args:
        await update.message.reply_text(
            "Usage: `/service_restart <service_name>`\n"
            "Contoh: `/service_restart nginx`\n\n"
            "⚠️ Bot harus dijalankan dengan sudo!",
            parse_mode='Markdown'
        )
        return
    
    service_name = context.args[0]
    info = restart_service(service_name)
    await update.message.reply_text(info, parse_mode='Markdown')
