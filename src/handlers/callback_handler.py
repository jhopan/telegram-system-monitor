"""
Callback Query Handler
Untuk inline keyboard buttons dengan navigasi lengkap
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from src.utils.decorators import require_admin_callback
from src.modules.system import (
    get_system_info, get_cpu_info, get_memory_info, 
    get_uptime, get_processes_info, get_users_info
)
from src.modules.network import (
    get_network_info, get_network_stats, get_public_ip,
    get_connections, get_routing_table, get_dns_info
)
from src.modules.disk import get_disk_info, get_partitions_info, get_disk_io_stats
from src.modules.service import list_services
from src.modules.device import get_device_info, get_sensors_info, get_battery_info
from src.handlers.chart_handlers import handle_chart_callback


@require_admin_callback
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk inline keyboard buttons dengan navigasi lengkap"""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    
    # Navigation handlers
    if callback_data == 'main_menu':
        await show_main_menu(query)
    elif callback_data == 'show_help':
        await show_help(query)
    elif callback_data == 'show_about':
        await show_about(query)
    elif callback_data == 'menu_system':
        await show_system_menu(query)
    elif callback_data == 'menu_disk':
        await show_disk_menu(query)
    elif callback_data == 'menu_network':
        await show_network_menu(query)
    elif callback_data == 'menu_service':
        await show_service_menu(query)
    elif callback_data == 'menu_device':
        await show_device_menu(query)
    elif callback_data == 'menu_tools':
        await show_tools_menu(query)
    elif callback_data == 'menu_charts':
        await show_charts_menu(query)
    # Chart handlers
    elif callback_data == 'chart_cpu':
        await handle_chart_callback(query, 'cpu')
    elif callback_data == 'chart_memory':
        await handle_chart_callback(query, 'memory')
    elif callback_data == 'chart_disk':
        await handle_chart_callback(query, 'disk')
    elif callback_data == 'chart_network':
        await handle_chart_callback(query, 'network')
    # System commands
    elif callback_data == 'system_info':
        await execute_and_show(query, get_system_info, "💻 SYSTEM INFO", 'menu_system')
    elif callback_data == 'system_cpu':
        await execute_and_show(query, get_cpu_info, "🔥 CPU INFO", 'menu_system')
    elif callback_data == 'system_memory':
        await execute_and_show(query, get_memory_info, "🧠 MEMORY INFO", 'menu_system')
    elif callback_data == 'system_uptime':
        await execute_and_show(query, get_uptime, "⏰ UPTIME", 'menu_system')
    elif callback_data == 'system_processes':
        await execute_and_show(query, get_processes_info, "📊 TOP PROCESSES", 'menu_system')
    elif callback_data == 'system_users':
        await execute_and_show(query, get_users_info, "👥 LOGGED USERS", 'menu_system')
    # Disk commands
    elif callback_data == 'disk_info':
        await execute_and_show(query, get_disk_info, "💾 DISK INFO", 'menu_disk')
    elif callback_data == 'disk_partitions':
        await execute_and_show(query, get_partitions_info, "📂 PARTITIONS", 'menu_disk')
    elif callback_data == 'disk_io':
        await execute_and_show(query, get_disk_io_stats, "💿 DISK I/O", 'menu_disk')
    # Network commands
    elif callback_data == 'network_info':
        await execute_and_show(query, get_network_info, "🌐 NETWORK INFO", 'menu_network')
    elif callback_data == 'network_stats':
        await execute_and_show(query, get_network_stats, "📈 NETWORK STATS", 'menu_network')
    elif callback_data == 'network_publicip':
        await execute_and_show(query, get_public_ip, "🌍 PUBLIC IP", 'menu_network')
    elif callback_data == 'network_connections':
        await execute_and_show(query, get_connections, "🔌 CONNECTIONS", 'menu_network')
    elif callback_data == 'network_routing':
        await execute_and_show(query, get_routing_table, "🛣️ ROUTING TABLE", 'menu_network')
    elif callback_data == 'network_dns':
        await execute_and_show(query, get_dns_info, "🔍 DNS INFO", 'menu_network')
    # Service commands
    elif callback_data == 'service_all':
        await execute_and_show(query, lambda: list_services(), "⚙️ ALL SERVICES", 'menu_service')
    elif callback_data == 'service_running':
        await execute_and_show(query, lambda: list_services('running'), "✅ RUNNING SERVICES", 'menu_service')
    elif callback_data == 'service_failed':
        await execute_and_show(query, lambda: list_services('failed'), "❌ FAILED SERVICES", 'menu_service')
    # Device commands
    elif callback_data == 'device_info':
        await execute_and_show(query, get_device_info, "🔧 DEVICE INFO", 'menu_device')
    elif callback_data == 'device_sensors':
        await execute_and_show(query, get_sensors_info, "🌡️ SENSORS", 'menu_device')
    elif callback_data == 'device_battery':
        await execute_and_show(query, get_battery_info, "🔋 BATTERY", 'menu_device')
    else:
        await query.edit_message_text("❌ Unknown command")


async def execute_and_show(query, func, title, back_menu):
    """Execute function dan show hasil dengan back button"""
    try:
        # Show loading
        await query.edit_message_text(f"⏳ Loading {title}...")
        
        # Execute function
        result = func()
        
        # Add title
        message = f"*{title}*\n\n{result}"
        
        # Create back button
        keyboard = [
            [InlineKeyboardButton("◀️ Back", callback_data=back_menu)],
            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send result (handle long messages)
        if len(message) > 4000:
            chunks = [message[i:i+4000] for i in range(0, len(message), 4000)]
            for i, chunk in enumerate(chunks):
                if i == 0:
                    await query.edit_message_text(
                        chunk,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=None
                    )
                elif i == len(chunks) - 1:
                    await query.message.reply_text(
                        chunk,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=reply_markup
                    )
                else:
                    await query.message.reply_text(
                        chunk,
                        parse_mode=ParseMode.MARKDOWN
                    )
        else:
            await query.edit_message_text(
                message,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
    except Exception as e:
        keyboard = [[InlineKeyboardButton("◀️ Back", callback_data=back_menu)]]
        await query.edit_message_text(
            f"❌ Error: {str(e)}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )



async def show_main_menu(query):
    """Tampilkan main menu"""
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
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_system_menu(query):
    """Tampilkan system submenu"""
    text = "💻 *SYSTEM MONITORING*\n\nPilih informasi yang ingin dilihat:"
    keyboard = [
        [
            InlineKeyboardButton("📋 System Info", callback_data='system_info'),
            InlineKeyboardButton("🔥 CPU", callback_data='system_cpu')
        ],
        [
            InlineKeyboardButton("🧠 Memory", callback_data='system_memory'),
            InlineKeyboardButton("⏰ Uptime", callback_data='system_uptime')
        ],
        [
            InlineKeyboardButton("📊 Processes", callback_data='system_processes'),
            InlineKeyboardButton("👥 Users", callback_data='system_users')
        ],
        [InlineKeyboardButton("◀️ Back to Main", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_disk_menu(query):
    """Tampilkan disk submenu"""
    text = "💾 *DISK MONITORING*\n\nPilih informasi yang ingin dilihat:"
    keyboard = [
        [
            InlineKeyboardButton("📊 Disk Usage", callback_data='disk_info'),
            InlineKeyboardButton("📂 Partitions", callback_data='disk_partitions')
        ],
        [
            InlineKeyboardButton("💿 Disk I/O", callback_data='disk_io'),
        ],
        [InlineKeyboardButton("◀️ Back to Main", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_network_menu(query):
    """Tampilkan network submenu"""
    text = "🌐 *NETWORK MONITORING*\n\nPilih informasi yang ingin dilihat:"
    keyboard = [
        [
            InlineKeyboardButton("📡 Interfaces", callback_data='network_info'),
            InlineKeyboardButton("📈 Statistics", callback_data='network_stats')
        ],
        [
            InlineKeyboardButton("🌍 Public IP", callback_data='network_publicip'),
            InlineKeyboardButton("🔌 Connections", callback_data='network_connections')
        ],
        [
            InlineKeyboardButton("🛣️ Routing", callback_data='network_routing'),
            InlineKeyboardButton("🔍 DNS", callback_data='network_dns')
        ],
        [InlineKeyboardButton("◀️ Back to Main", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_service_menu(query):
    """Tampilkan service submenu"""
    text = "⚙️ *SERVICE MANAGEMENT*\n\nPilih kategori service:"
    keyboard = [
        [
            InlineKeyboardButton("📋 All Services", callback_data='service_all'),
        ],
        [
            InlineKeyboardButton("✅ Running", callback_data='service_running'),
            InlineKeyboardButton("❌ Failed", callback_data='service_failed')
        ],
        [InlineKeyboardButton("◀️ Back to Main", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_device_menu(query):
    """Tampilkan device submenu"""
    text = "🔧 *DEVICE INFORMATION*\n\nPilih informasi device:"
    keyboard = [
        [
            InlineKeyboardButton("💻 Hardware", callback_data='device_info'),
            InlineKeyboardButton("🌡️ Sensors", callback_data='device_sensors')
        ],
        [
            InlineKeyboardButton("🔋 Battery", callback_data='device_battery'),
        ],
        [InlineKeyboardButton("◀️ Back to Main", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_tools_menu(query):
    """Tampilkan tools submenu"""
    text = "🛠️ *TOOLS & UTILITIES*\n\nFitur tambahan:"
    keyboard = [
        [
            InlineKeyboardButton("📊 Charts", callback_data='menu_charts'),
            InlineKeyboardButton("🔔 Alerts (Soon)", callback_data='tools_alerts')
        ],
        [
            InlineKeyboardButton("📝 Reports (Soon)", callback_data='tools_reports'),
            InlineKeyboardButton("🐳 Docker (Soon)", callback_data='tools_docker')
        ],
        [InlineKeyboardButton("◀️ Back to Main", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_charts_menu(query):
    """Tampilkan charts submenu"""
    text = "📊 *CHARTS & VISUALIZATION*\n\nGenerate visual charts:"
    keyboard = [
        [
            InlineKeyboardButton("🔥 CPU Chart", callback_data='chart_cpu'),
            InlineKeyboardButton("🧠 Memory Chart", callback_data='chart_memory')
        ],
        [
            InlineKeyboardButton("💾 Disk Chart", callback_data='chart_disk'),
            InlineKeyboardButton("🌐 Network Chart", callback_data='chart_network')
        ],
        [InlineKeyboardButton("◀️ Back to Tools", callback_data='menu_tools')],
        [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_help(query):
    """Tampilkan help"""
    text = """
📚 *HELP - CARA PENGGUNAAN*

*Navigasi:*
• Gunakan tombol inline keyboard untuk navigasi
• Tombol "Back" untuk kembali ke menu sebelumnya
• Tombol "Main Menu" untuk kembali ke menu utama

*Kategori:*
• 💻 *System* - CPU, Memory, Uptime, Processes, Users
• 💾 *Disk* - Disk usage, Partitions, I/O Stats
• 🌐 *Network* - Interfaces, Stats, Connections, DNS
• ⚙️ *Services* - Service management & monitoring
• 🔧 *Device* - Hardware info, Sensors, Battery
• 🛠️ *Tools* - Advanced features (coming soon)

*Text Commands:*
Anda juga bisa menggunakan text commands seperti:
`/cpu` `/memory` `/disk` `/network` `/services`

Type `/help` untuk daftar lengkap commands.
"""
    keyboard = [[InlineKeyboardButton("◀️ Back", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_about(query):
    """Tampilkan about"""
    text = """
ℹ️ *ABOUT*

*Telegram System Monitor Bot*
Version: 2.0

Bot monitoring sistem Linux/Debian yang powerful dan mudah digunakan.

*Features:*
✅ Real-time monitoring
✅ Interactive inline keyboard
✅ Admin authentication
✅ Modular architecture
✅ Service management
✅ Network tools

*Tech Stack:*
• Python 3.8+
• python-telegram-bot
• psutil
• systemd

*Repository:*
github.com/jhopan/telegram-system-monitor

*License:* MIT License
*Author:* jhopan
"""
    keyboard = [[InlineKeyboardButton("◀️ Back", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

