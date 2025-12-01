"""
Callback Query Handler
Untuk inline keyboard buttons
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from src.utils.decorators import require_admin_callback
from src.modules.system import get_system_info, get_memory_info, get_uptime, get_processes_info
from src.modules.network import get_network_info, get_network_stats, get_public_ip
from src.modules.disk import get_disk_info
from src.modules.service import list_services
from src.modules.device import get_device_info, get_battery_info


@require_admin_callback
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk inline keyboard buttons"""
    query = update.callback_query
    await query.answer()
    
    # Map callback data to functions
    handlers = {
        'system': lambda: get_system_info(),
        'memory': lambda: get_memory_info(),
        'disk': lambda: get_disk_info(),
        'uptime': lambda: get_uptime(),
        'processes': lambda: get_processes_info(),
        'network': lambda: get_network_info(),
        'netstats': lambda: get_network_stats(),
        'publicip': lambda: get_public_ip(),
        'services': lambda: list_services(),
        'services_failed': lambda: list_services('failed'),
        'device': lambda: get_device_info(),
        'battery': lambda: get_battery_info(),
    }
    
    callback_data = query.data
    
    if callback_data == 'menu':
        await show_menu(query)
        return
    
    if callback_data in handlers:
        # Show loading message
        await query.edit_message_text("⏳ Mengambil data...")
        
        # Get info
        info = handlers[callback_data]()
        
        # Add back to menu button
        keyboard = [[InlineKeyboardButton("◀️ Kembali ke Menu", callback_data='menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send info (split if too long)
        if len(info) > 4000:
            chunks = [info[i:i+4000] for i in range(0, len(info), 4000)]
            for i, chunk in enumerate(chunks):
                if i == len(chunks) - 1:
                    await query.message.reply_text(
                        chunk,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=reply_markup
                    )
                else:
                    await query.message.reply_text(chunk, parse_mode=ParseMode.MARKDOWN)
            # Delete loading message
            await query.message.delete()
        else:
            await query.edit_message_text(
                info,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )


async def show_menu(query):
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
    
    await query.edit_message_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
