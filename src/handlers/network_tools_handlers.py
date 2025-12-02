"""
Network Tools Handlers Module

Provides inline keyboard handlers for advanced network tools.
Full button interface - no typing required!
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from src.modules.network_tools import NetworkTools


async def show_network_tools_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main network tools menu"""
    query = update.callback_query
    if query:
        await query.answer()
    
    text = (
        "🌐 <b>Network Tools Advanced</b>\n\n"
        "Diagnostic & testing tools untuk network:\n\n"
        "Pilih tool:"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🏓 Ping", callback_data="nettools_ping"),
            InlineKeyboardButton("🛤️ Traceroute", callback_data="nettools_trace")
        ],
        [
            InlineKeyboardButton("🔍 Port Scanner", callback_data="nettools_portscan"),
            InlineKeyboardButton("🌐 DNS Lookup", callback_data="nettools_dns")
        ],
        [
            InlineKeyboardButton("📋 Whois", callback_data="nettools_whois"),
            InlineKeyboardButton("🔍 Resolve Host", callback_data="nettools_resolve")
        ],
        [
            InlineKeyboardButton("◀️ Back to Tools", callback_data="menu_tools")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_ping_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show ping tool menu with common hosts"""
    query = update.callback_query
    await query.answer()
    
    net_tools = NetworkTools()
    common_hosts = net_tools.get_common_hosts()
    
    text = (
        "🏓 <b>Ping Tool</b>\n\n"
        "Test network connectivity ke host:\n\n"
        "Pilih host atau category:"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🌐 DNS Servers", callback_data="nettools_ping_cat_dns"),
            InlineKeyboardButton("🌍 Websites", callback_data="nettools_ping_cat_websites")
        ],
        [
            InlineKeyboardButton("🏠 Local Network", callback_data="nettools_ping_cat_local")
        ],
        [
            InlineKeyboardButton("◀️ Back", callback_data="nettools_menu")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_ping_category(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
    """Show hosts in ping category"""
    query = update.callback_query
    await query.answer()
    
    net_tools = NetworkTools()
    common_hosts = net_tools.get_common_hosts()
    
    category_labels = {
        'dns': '🌐 DNS Servers',
        'websites': '🌍 Websites',
        'local': '🏠 Local Network'
    }
    
    hosts = common_hosts.get(category, {})
    title = category_labels.get(category, category)
    
    text = f"<b>{title}</b>\n\nSelect host to ping:"
    
    keyboard = []
    for host_key, host_info in hosts.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{host_info['name']} ({host_info['host']})",
                callback_data=f"nettools_ping_exec_{host_info['host']}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton("◀️ Back", callback_data="nettools_ping")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def execute_ping(update: Update, context: ContextTypes.DEFAULT_TYPE, host: str):
    """Execute ping to host"""
    query = update.callback_query
    await query.answer(f"Pinging {host}...")
    
    # Show progress message
    await query.edit_message_text(
        f"🏓 <b>Pinging {host}...</b>\n\n"
        f"⏳ Please wait...",
        parse_mode=ParseMode.HTML
    )
    
    net_tools = NetworkTools()
    result = net_tools.ping_host(host, count=4)
    formatted = net_tools.format_ping_result(result)
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Ping Again", callback_data=f"nettools_ping_exec_{host}"),
            InlineKeyboardButton("🛤️ Traceroute", callback_data=f"nettools_trace_exec_{host}")
        ],
        [
            InlineKeyboardButton("◀️ Back", callback_data="nettools_ping")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(formatted, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_traceroute_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show traceroute menu"""
    query = update.callback_query
    await query.answer()
    
    text = (
        "🛤️ <b>Traceroute Tool</b>\n\n"
        "Trace network path ke host:\n\n"
        "Pilih host category:"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🌐 DNS Servers", callback_data="nettools_trace_cat_dns"),
            InlineKeyboardButton("🌍 Websites", callback_data="nettools_trace_cat_websites")
        ],
        [
            InlineKeyboardButton("◀️ Back", callback_data="nettools_menu")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_traceroute_category(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
    """Show hosts in traceroute category"""
    query = update.callback_query
    await query.answer()
    
    net_tools = NetworkTools()
    common_hosts = net_tools.get_common_hosts()
    
    category_labels = {
        'dns': '🌐 DNS Servers',
        'websites': '🌍 Websites'
    }
    
    hosts = common_hosts.get(category, {})
    title = category_labels.get(category, category)
    
    text = f"<b>{title}</b>\n\nSelect host for traceroute:"
    
    keyboard = []
    for host_key, host_info in hosts.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{host_info['name']} ({host_info['host']})",
                callback_data=f"nettools_trace_exec_{host_info['host']}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton("◀️ Back", callback_data="nettools_trace")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def execute_traceroute(update: Update, context: ContextTypes.DEFAULT_TYPE, host: str):
    """Execute traceroute to host"""
    query = update.callback_query
    await query.answer(f"Tracing route to {host}...")
    
    await query.edit_message_text(
        f"🛤️ <b>Traceroute to {host}...</b>\n\n"
        f"⏳ This may take up to 60 seconds...",
        parse_mode=ParseMode.HTML
    )
    
    net_tools = NetworkTools()
    result = net_tools.traceroute(host, max_hops=20)
    formatted = net_tools.format_traceroute_result(result, max_lines=15)
    
    keyboard = [
        [
            InlineKeyboardButton("🏓 Ping", callback_data=f"nettools_ping_exec_{host}"),
            InlineKeyboardButton("◀️ Back", callback_data="nettools_trace")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(formatted, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_portscan_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show port scanner menu"""
    query = update.callback_query
    await query.answer()
    
    text = (
        "🔍 <b>Port Scanner</b>\n\n"
        "Scan ports on a host:\n\n"
        "Pilih port category:"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🌐 Web Ports", callback_data="nettools_port_cat_web"),
            InlineKeyboardButton("🔐 Remote Access", callback_data="nettools_port_cat_remote")
        ],
        [
            InlineKeyboardButton("🗄️ Database Ports", callback_data="nettools_port_cat_database"),
            InlineKeyboardButton("📧 Mail Ports", callback_data="nettools_port_cat_mail")
        ],
        [
            InlineKeyboardButton("🔧 Other Ports", callback_data="nettools_port_cat_other")
        ],
        [
            InlineKeyboardButton("◀️ Back", callback_data="nettools_menu")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_portscan_category(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
    """Show ports in category"""
    query = update.callback_query
    await query.answer()
    
    net_tools = NetworkTools()
    common_ports = net_tools.get_common_ports()
    
    category_labels = {
        'web': '🌐 Web Ports',
        'remote': '🔐 Remote Access',
        'database': '🗄️ Database Ports',
        'mail': '📧 Mail Ports',
        'other': '🔧 Other Ports'
    }
    
    ports = common_ports.get(category, {})
    title = category_labels.get(category, category)
    
    text = f"<b>{title}</b>\n\nSelect port to scan on localhost:"
    
    keyboard = []
    for port_key, port_info in ports.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{port_info['name']} (:{port_info['port']})",
                callback_data=f"nettools_port_scan_localhost_{port_info['port']}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton("◀️ Back", callback_data="nettools_portscan")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def execute_portscan(update: Update, context: ContextTypes.DEFAULT_TYPE, host: str, port: int):
    """Execute port scan"""
    query = update.callback_query
    await query.answer(f"Scanning port {port}...")
    
    net_tools = NetworkTools()
    result = net_tools.port_scan(host, port, timeout=3.0)
    
    if result['open']:
        status = "✅ <b>OPEN</b>"
        service_info = f"\n🔧 <b>Service:</b> {result['service']}" if result.get('service') else ""
    else:
        status = "❌ <b>CLOSED</b>"
        service_info = ""
    
    text = (
        f"🔍 <b>Port Scan Result</b>\n\n"
        f"🌐 <b>Host:</b> <code>{host}</code>\n"
        f"🔌 <b>Port:</b> {port}\n"
        f"📊 <b>Status:</b> {status}{service_info}"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Scan Again", callback_data=f"nettools_port_scan_{host}_{port}"),
            InlineKeyboardButton("◀️ Back", callback_data="nettools_portscan")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_dns_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show DNS lookup menu"""
    query = update.callback_query
    await query.answer()
    
    net_tools = NetworkTools()
    record_types = net_tools.get_dns_record_types()
    
    text = (
        "🌐 <b>DNS Lookup</b>\n\n"
        "Query DNS records:\n\n"
        "Select record type:"
    )
    
    keyboard = []
    for rtype, label in record_types.items():
        keyboard.append([
            InlineKeyboardButton(label, callback_data=f"nettools_dns_type_{rtype}")
        ])
    
    keyboard.append([
        InlineKeyboardButton("◀️ Back", callback_data="nettools_menu")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_dns_type_hosts(update: Update, context: ContextTypes.DEFAULT_TYPE, record_type: str):
    """Show common domains for DNS lookup"""
    query = update.callback_query
    await query.answer()
    
    net_tools = NetworkTools()
    record_types = net_tools.get_dns_record_types()
    type_label = record_types.get(record_type, record_type)
    
    text = (
        f"<b>{type_label}</b>\n\n"
        f"Select domain to query:"
    )
    
    # Common domains
    domains = {
        'google.com': '🔍 Google',
        'github.com': '🐙 GitHub',
        'cloudflare.com': '☁️ Cloudflare',
        'facebook.com': '📘 Facebook',
        'twitter.com': '🐦 Twitter'
    }
    
    keyboard = []
    for domain, label in domains.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{label} ({domain})",
                callback_data=f"nettools_dns_query_{record_type}_{domain}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton("◀️ Back", callback_data="nettools_dns")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def execute_dns_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE, domain: str, record_type: str):
    """Execute DNS lookup"""
    query = update.callback_query
    await query.answer(f"Looking up {record_type} records...")
    
    await query.edit_message_text(
        f"🌐 <b>DNS Lookup...</b>\n\n"
        f"⏳ Querying {record_type} records for {domain}...",
        parse_mode=ParseMode.HTML
    )
    
    net_tools = NetworkTools()
    result = net_tools.dns_lookup(domain, record_type)
    formatted = net_tools.format_dns_result(result)
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Query Again", callback_data=f"nettools_dns_query_{record_type}_{domain}"),
            InlineKeyboardButton("◀️ Back", callback_data="nettools_dns")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(formatted, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


# Command handler
async def network_tools_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /networktools command"""
    await show_network_tools_menu(update, context)
