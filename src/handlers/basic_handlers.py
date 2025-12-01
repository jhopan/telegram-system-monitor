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
    """Handler untuk command /start dengan inline keyboard"""
    welcome_text = """
🤖 *TELEGRAM SYSTEM MONITOR*

Selamat datang! Bot ini membantu Anda memonitor sistem Linux/Debian secara real-time langsung dari Telegram.

*✨ Fitur Utama:*
• 💻 System monitoring (CPU, Memory, Uptime)
• 💾 Disk monitoring (Usage, Partitions, I/O)
• 🌐 Network monitoring (Interfaces, Connections)
• ⚙️ Service management
• 🔧 Device information

*Klik tombol di bawah untuk mulai monitoring!*
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🚀 Start Monitoring", callback_data='main_menu')
        ],
        [
            InlineKeyboardButton("📚 Help", callback_data='show_help'),
            InlineKeyboardButton("ℹ️ About", callback_data='show_about')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
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
    """Tampilkan main menu interaktif"""
    text = """
🤖 *TELEGRAM SYSTEM MONITOR*

Pilih kategori monitoring:
"""
    keyboard = [
        [
            InlineKeyboardButton("💻 System", callback_data='menu_system'),
            InlineKeyboardButton("💾 Disk", callback_data='menu_disk')
        ],
        [
            InlineKeyboardButton("🌐 Network", callback_data='menu_network'),
            InlineKeyboardButton("⚙️ Services", callback_data='menu_service')
        ],
        [
            InlineKeyboardButton("🔧 Device", callback_data='menu_device'),
            InlineKeyboardButton("🛠️ Tools", callback_data='menu_tools')
        ],
        [InlineKeyboardButton("🔄 Refresh", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


@require_admin
async def admin_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tampilkan informasi admin configuration"""
    info = config.get_admin_info()
    await update.message.reply_text(info, parse_mode=ParseMode.MARKDOWN)

