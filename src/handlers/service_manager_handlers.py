"""
Advanced Service Handlers Module

Provides inline keyboard handlers for advanced service management.
Full button interface - no typing required!
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from src.modules.service.advanced_manager import ServiceManager


async def show_service_manager_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main service manager menu"""
    query = update.callback_query
    if query:
        await query.answer()
    
    service_manager = ServiceManager()
    counts = service_manager.get_service_counts()
    
    text = (
        "⚙️ <b>Service Manager Advanced</b>\n\n"
        f"📊 <b>Service Overview:</b>\n"
        f"  • Total: {counts['total']}\n"
        f"  • 🟢 Running: {counts['running']}\n"
        f"  • ❌ Failed: {counts['failed']}\n"
        f"  • ⭕ Inactive: {counts['inactive']}\n\n"
        "Pilih opsi:"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("📋 All Services", callback_data="svcmgr_list_all"),
            InlineKeyboardButton("🟢 Running", callback_data="svcmgr_list_running")
        ],
        [
            InlineKeyboardButton("❌ Failed", callback_data="svcmgr_list_failed"),
            InlineKeyboardButton("⭕ Inactive", callback_data="svcmgr_list_inactive")
        ],
        [
            InlineKeyboardButton("✅ Enabled", callback_data="svcmgr_list_enabled"),
            InlineKeyboardButton("🚫 Disabled", callback_data="svcmgr_list_disabled")
        ],
        [
            InlineKeyboardButton("🔍 Common Services", callback_data="svcmgr_common")
        ],
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="svcmgr_menu"),
            InlineKeyboardButton("◀️ Back to Tools", callback_data="menu_tools")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_services_list(update: Update, context: ContextTypes.DEFAULT_TYPE, filter_type: str):
    """Show list of services with filter"""
    query = update.callback_query
    await query.answer()
    
    service_manager = ServiceManager()
    services = service_manager.get_services_list(filter_type)
    
    filter_labels = {
        'all': '📋 All Services',
        'running': '🟢 Running Services',
        'failed': '❌ Failed Services',
        'inactive': '⭕ Inactive Services',
        'enabled': '✅ Enabled Services',
        'disabled': '🚫 Disabled Services'
    }
    
    title = filter_labels.get(filter_type, 'Services')
    
    if not services:
        text = f"<b>{title}</b>\n\n<i>No services found.</i>"
        keyboard = [[InlineKeyboardButton("◀️ Back", callback_data="svcmgr_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        return
    
    # Pagination - 15 per page
    page = context.user_data.get('svcmgr_page', 0)
    per_page = 15
    start_idx = page * per_page
    end_idx = start_idx + per_page
    page_services = services[start_idx:end_idx]
    
    text = f"<b>{title}</b>\n\n"
    text += f"Showing {start_idx + 1}-{min(end_idx, len(services))} of {len(services)} services:\n\n"
    
    keyboard = []
    for svc in page_services:
        icon = service_manager.get_status_icon(svc['active'])
        button_text = f"{icon} {svc['name'][:25]}"
        keyboard.append([
            InlineKeyboardButton(button_text, callback_data=f"svcmgr_detail_{svc['name']}")
        ])
    
    # Pagination buttons
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("◀️ Prev", callback_data=f"svcmgr_page_{filter_type}_{page-1}"))
    if end_idx < len(services):
        nav_buttons.append(InlineKeyboardButton("Next ▶️", callback_data=f"svcmgr_page_{filter_type}_{page+1}"))
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([
        InlineKeyboardButton("🔄 Refresh", callback_data=f"svcmgr_list_{filter_type}"),
        InlineKeyboardButton("◀️ Back", callback_data="svcmgr_menu")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_service_detail(update: Update, context: ContextTypes.DEFAULT_TYPE, service_name: str):
    """Show detailed information about a service"""
    query = update.callback_query
    await query.answer("Loading service details...")
    
    service_manager = ServiceManager()
    details = service_manager.get_service_detail(service_name)
    
    icon = service_manager.get_status_icon(details['active'])
    
    text = (
        f"{icon} <b>{details['name']}</b>\n\n"
        f"<b>Status:</b> {details['status']}\n"
        f"<b>Enabled:</b> {details['enabled']}\n"
        f"<b>Loaded:</b> {details['loaded'][:60]}...\n\n"
    )
    
    if details['pid'] != 'N/A':
        text += f"<b>PID:</b> {details['pid']}\n"
    if details['memory'] != 'N/A':
        text += f"<b>Memory:</b> {details['memory']}\n"
    if details['cpu'] != 'N/A':
        text += f"<b>CPU:</b> {details['cpu']}\n"
    
    if details['description'] != 'N/A':
        text += f"\n<i>{details['description'][:100]}</i>"
    
    # Control buttons based on status
    keyboard = []
    
    if details['active'] == 'active':
        keyboard.append([
            InlineKeyboardButton("🛑 Stop", callback_data=f"svcmgr_stop_{service_name}"),
            InlineKeyboardButton("🔄 Restart", callback_data=f"svcmgr_restart_{service_name}")
        ])
        keyboard.append([
            InlineKeyboardButton("🔁 Reload", callback_data=f"svcmgr_reload_{service_name}")
        ])
    else:
        keyboard.append([
            InlineKeyboardButton("▶️ Start", callback_data=f"svcmgr_start_{service_name}")
        ])
    
    if details['enabled'] == 'enabled':
        keyboard.append([
            InlineKeyboardButton("🚫 Disable", callback_data=f"svcmgr_disable_{service_name}")
        ])
    else:
        keyboard.append([
            InlineKeyboardButton("✅ Enable", callback_data=f"svcmgr_enable_{service_name}")
        ])
    
    keyboard.append([
        InlineKeyboardButton("📜 View Logs", callback_data=f"svcmgr_logs_{service_name}"),
        InlineKeyboardButton("🔗 Dependencies", callback_data=f"svcmgr_deps_{service_name}")
    ])
    
    keyboard.append([
        InlineKeyboardButton("🔄 Refresh", callback_data=f"svcmgr_detail_{service_name}"),
        InlineKeyboardButton("◀️ Back", callback_data="svcmgr_menu")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_service_logs(update: Update, context: ContextTypes.DEFAULT_TYPE, service_name: str):
    """Show service logs"""
    query = update.callback_query
    await query.answer("Loading logs...")
    
    service_manager = ServiceManager()
    logs = service_manager.get_service_logs(service_name, lines=100)
    formatted_logs = service_manager.format_logs(logs)
    
    text = (
        f"<b>📜 Logs: {service_name}</b>\n\n"
        f"{formatted_logs}"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh", callback_data=f"svcmgr_logs_{service_name}"),
            InlineKeyboardButton("◀️ Back", callback_data=f"svcmgr_detail_{service_name}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_service_dependencies(update: Update, context: ContextTypes.DEFAULT_TYPE, service_name: str):
    """Show service dependencies"""
    query = update.callback_query
    await query.answer("Loading dependencies...")
    
    service_manager = ServiceManager()
    deps = service_manager.get_service_dependencies(service_name)
    
    # Format and truncate
    if len(deps) > 3000:
        deps = '\n'.join(deps.split('\n')[:40]) + '\n\n... truncated ...'
    
    text = (
        f"<b>🔗 Dependencies: {service_name}</b>\n\n"
        f"<pre>{deps}</pre>"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("◀️ Back", callback_data=f"svcmgr_detail_{service_name}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_common_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show common services menu"""
    query = update.callback_query
    await query.answer()
    
    text = (
        "<b>🔍 Common Services</b>\n\n"
        "Quick access to frequently used services:"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🌐 Web Servers", callback_data="svcmgr_cat_web"),
            InlineKeyboardButton("🗄️ Databases", callback_data="svcmgr_cat_database")
        ],
        [
            InlineKeyboardButton("⚙️ System Services", callback_data="svcmgr_cat_system"),
            InlineKeyboardButton("🛡️ Other Services", callback_data="svcmgr_cat_other")
        ],
        [
            InlineKeyboardButton("◀️ Back", callback_data="svcmgr_menu")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_common_category(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
    """Show services in a common category"""
    query = update.callback_query
    await query.answer()
    
    service_manager = ServiceManager()
    common_services = service_manager.get_common_services()
    
    category_labels = {
        'web': '🌐 Web Servers',
        'database': '🗄️ Databases',
        'system': '⚙️ System Services',
        'other': '🛡️ Other Services'
    }
    
    services = common_services.get(category, {})
    title = category_labels.get(category, category)
    
    text = f"<b>{title}</b>\n\nSelect a service:"
    
    keyboard = []
    for svc_name, svc_label in services.items():
        keyboard.append([
            InlineKeyboardButton(svc_label, callback_data=f"svcmgr_detail_{svc_name}")
        ])
    
    keyboard.append([
        InlineKeyboardButton("◀️ Back", callback_data="svcmgr_common")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def handle_service_action(update: Update, context: ContextTypes.DEFAULT_TYPE, service_name: str, action: str):
    """Handle service control actions"""
    query = update.callback_query
    await query.answer(f"{action.capitalize()}ing service...")
    
    service_manager = ServiceManager()
    success, message = service_manager.control_service(service_name, action)
    
    # Show result
    icon = "✅" if success else "❌"
    result_text = f"{icon} <b>{message}</b>"
    
    # Redirect back to detail with result
    await query.answer(message, show_alert=True)
    await show_service_detail(update, context, service_name)


async def confirm_service_action(update: Update, context: ContextTypes.DEFAULT_TYPE, service_name: str, action: str):
    """Show confirmation for destructive actions"""
    query = update.callback_query
    await query.answer()
    
    action_labels = {
        'stop': '🛑 Stop',
        'restart': '🔄 Restart',
        'disable': '🚫 Disable'
    }
    
    label = action_labels.get(action, action)
    
    text = (
        f"<b>⚠️ Confirmation Required</b>\n\n"
        f"Are you sure you want to <b>{action}</b> service:\n"
        f"<code>{service_name}</code>?"
    )
    
    keyboard = [
        [
            InlineKeyboardButton(f"✅ Yes, {label}", callback_data=f"svcmgr_confirm_{action}_{service_name}"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"svcmgr_detail_{service_name}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


# Command handler
async def service_manager_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /servicemanager command"""
    await show_service_manager_menu(update, context)
