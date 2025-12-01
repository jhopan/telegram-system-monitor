"""
Basic Handlers (Start, Help, Menu, Admin)
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from src.utils.decorators import require_admin
from config.settings import config
import logging

logger = logging.getLogger(__name__)


@require_admin
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /start"""
    welcome_text = """
🤖 *Bot Monitoring Sistem Linux*

Bot ini membantu Anda memonitor sistem Linux/Debian secara real-time.

*📋 KATEGORI COMMANDS:*

*System Info:* /system, /cpu, /memory, /uptime
*Disk:* /disk, /partitions, /diskio
*Network:* /network, /netstats, /connections
*Service:* /services, /service_status
*Device:* /device, /sensors, /battery

*Gunakan /menu untuk navigasi interaktif!*
*Gunakan /help untuk daftar lengkap commands*
"""
    
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN
    )


@require_admin
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /help"""
    help_text = """
📚 *DAFTAR LENGKAP COMMANDS*

*SISTEM INFO:*
/system - Info sistem lengkap
/cpu - Info CPU usage
/memory - Info RAM dan SWAP
/uptime - Uptime sistem
/processes - Top proses yang berjalan
/users - User yang sedang login

*DISK:*
/disk - Info disk dan partisi
/partitions - Info detail partisi
/diskio - Statistik disk IO

*NETWORK:*
/network - Info network interface
/netstats - Statistik jaringan
/connections - Koneksi aktif
/publicip - IP public
/ping <host> - Ping ke host
/route - Routing table
/dns - Info DNS

*SERVICE MANAGEMENT:*
/services - List semua services
/services_running - List running services
/services_failed - List failed services
/service_status <name> - Status detail service
/service_logs <name> [lines] - Logs service
/service_start <name> - Start service (perlu sudo)
/service_stop <name> - Stop service (perlu sudo)
/service_restart <name> - Restart service (perlu sudo)

*DEVICE:*
/device - Info device/hardware
/sensors - Info sensors (temperature, fans)
/battery - Info battery (untuk laptop)

*LAINNYA:*
/menu - Menu interaktif
/admininfo - Info konfigurasi admin
/help - Bantuan
"""
    
    await update.message.reply_text(
        help_text,
        parse_mode=ParseMode.MARKDOWN
    )


@require_admin
async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tampilkan menu interaktif"""
    keyboard = [
        [
            InlineKeyboardButton("💻 System", callback_data='system'),
            InlineKeyboardButton("🧠 Memory", callback_data='memory')
        ],
        [
            InlineKeyboardButton("💾 Disk", callback_data='disk'),
            InlineKeyboardButton("⏰ Uptime", callback_data='uptime')
        ],
        [
            InlineKeyboardButton("🌐 Network", callback_data='network'),
            InlineKeyboardButton("📈 Net Stats", callback_data='netstats')
        ],
        [
            InlineKeyboardButton("⚙️ Services", callback_data='services'),
            InlineKeyboardButton("❌ Failed Services", callback_data='services_failed')
        ],
        [
            InlineKeyboardButton("📊 Top Processes", callback_data='processes'),
            InlineKeyboardButton("🌍 Public IP", callback_data='publicip')
        ],
        [
            InlineKeyboardButton("🔧 Device Info", callback_data='device'),
            InlineKeyboardButton("🔋 Battery", callback_data='battery')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = "🤖 *Menu Monitoring Sistem*\n\nPilih informasi yang ingin Anda lihat:"
    
    await update.message.reply_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


@require_admin
async def admin_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tampilkan informasi admin configuration"""
    info = config.get_admin_info()
    await update.message.reply_text(info, parse_mode=ParseMode.MARKDOWN)
