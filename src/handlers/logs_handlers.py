"""
Logs Handlers Module

Provides inline keyboard handlers for logs viewing.
Full button interface - no typing required!
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from src.modules.logs import LogsManager


async def show_logs_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main logs menu"""
    query = update.callback_query
    if query:
        await query.answer()
    
    logs_manager = LogsManager()
    
    # Get log summary
    summary = logs_manager.get_log_summary()
    
    text = (
        "📊 <b>System Logs Viewer</b>\n\n"
        f"{summary}\n\n"
        "Pilih kategori logs yang ingin dilihat:"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🖥️ System Logs", callback_data="logs_type_system"),
            InlineKeyboardButton("🔐 Auth Logs", callback_data="logs_type_auth")
        ],
        [
            InlineKeyboardButton("⚙️ Kernel Logs", callback_data="logs_type_kernel"),
            InlineKeyboardButton("📋 Syslog", callback_data="logs_type_syslog")
        ],
        [
            InlineKeyboardButton("📱 Application Logs", callback_data="logs_apps")
        ],
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="logs_menu"),
            InlineKeyboardButton("◀️ Back to Tools", callback_data="menu_tools")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_log_type(update: Update, context: ContextTypes.DEFAULT_TYPE, log_type: str):
    """Show logs for a specific type"""
    query = update.callback_query
    await query.answer()
    
    logs_manager = LogsManager()
    
    # Show time range options first
    context.user_data['current_log_type'] = log_type
    
    log_info = logs_manager.LOG_TYPES.get(log_type, {})
    log_name = log_info.get('name', log_type)
    
    text = (
        f"<b>{log_name}</b>\n\n"
        "Pilih time range:"
    )
    
    time_ranges = logs_manager.get_time_ranges()
    keyboard = []
    
    for time_key, time_label in time_ranges.items():
        keyboard.append([
            InlineKeyboardButton(time_label, callback_data=f"logs_view_{log_type}_{time_key}")
        ])
    
    # Add 'All' option
    keyboard.append([
        InlineKeyboardButton("📜 All (Last 100 lines)", callback_data=f"logs_view_{log_type}_all")
    ])
    
    keyboard.append([
        InlineKeyboardButton("◀️ Back", callback_data="logs_menu")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_application_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show application logs selection"""
    query = update.callback_query
    await query.answer()
    
    logs_manager = LogsManager()
    
    text = (
        "📱 <b>Application Logs</b>\n\n"
        "Pilih aplikasi:"
    )
    
    apps = logs_manager.get_applications()
    keyboard = []
    
    for app_key, app_label in apps.items():
        keyboard.append([
            InlineKeyboardButton(app_label, callback_data=f"logs_app_{app_key}")
        ])
    
    keyboard.append([
        InlineKeyboardButton("◀️ Back", callback_data="logs_menu")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def view_application_logs(update: Update, context: ContextTypes.DEFAULT_TYPE, app_name: str):
    """View logs for specific application"""
    query = update.callback_query
    await query.answer("Loading logs...")
    
    logs_manager = LogsManager()
    app_label = logs_manager.APPLICATIONS.get(app_name, app_name)
    
    # Get logs
    logs = logs_manager.get_application_log(app_name, lines=100)
    formatted_logs = logs_manager.format_logs(logs)
    
    text = (
        f"<b>{app_label} Logs</b>\n\n"
        f"{formatted_logs}"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh", callback_data=f"logs_app_{app_name}"),
            InlineKeyboardButton("◀️ Back", callback_data="logs_apps")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def view_logs(update: Update, context: ContextTypes.DEFAULT_TYPE, log_type: str, time_range: str):
    """View logs with filters"""
    query = update.callback_query
    await query.answer("Loading logs...")
    
    logs_manager = LogsManager()
    log_info = logs_manager.LOG_TYPES.get(log_type, {})
    log_name = log_info.get('name', log_type)
    method = log_info.get('method', 'journal')
    
    # Get logs based on type
    if method == 'journal':
        since = None if time_range == 'all' else time_range
        logs = logs_manager.get_journal_logs(lines=100, since=since)
    elif method == 'auth':
        logs = logs_manager.get_auth_logs(lines=100)
    elif method == 'kernel':
        logs = logs_manager.get_kernel_logs(lines=100)
    elif method == 'syslog':
        logs = logs_manager.get_syslog(lines=100)
    else:
        logs = "Unknown log type"
    
    formatted_logs = logs_manager.format_logs(logs)
    
    time_label = logs_manager.TIME_RANGES.get(time_range, 'All')
    
    text = (
        f"<b>{log_name}</b>\n"
        f"⏱️ {time_label}\n\n"
        f"{formatted_logs}"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh", callback_data=f"logs_view_{log_type}_{time_range}"),
            InlineKeyboardButton("⏱️ Change Time", callback_data=f"logs_type_{log_type}")
        ],
        [
            InlineKeyboardButton("◀️ Back to Logs", callback_data="logs_menu")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def show_priority_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show priority filter options for system logs"""
    query = update.callback_query
    await query.answer()
    
    logs_manager = LogsManager()
    
    text = (
        "🔍 <b>Filter by Priority</b>\n\n"
        "Pilih level prioritas:"
    )
    
    priorities = logs_manager.get_priorities()
    keyboard = []
    
    for priority_key, priority_label in priorities.items():
        keyboard.append([
            InlineKeyboardButton(priority_label, callback_data=f"logs_priority_{priority_key}")
        ])
    
    keyboard.append([
        InlineKeyboardButton("◀️ Back", callback_data="logs_type_system")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def view_logs_by_priority(update: Update, context: ContextTypes.DEFAULT_TYPE, priority: str):
    """View logs filtered by priority"""
    query = update.callback_query
    await query.answer("Loading logs...")
    
    logs_manager = LogsManager()
    
    logs = logs_manager.get_journal_logs(lines=100, priority=priority)
    formatted_logs = logs_manager.format_logs(logs)
    
    priority_label = logs_manager.PRIORITIES.get(priority, priority)
    
    text = (
        f"<b>System Logs</b>\n"
        f"🔍 {priority_label}\n\n"
        f"{formatted_logs}"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh", callback_data=f"logs_priority_{priority}"),
            InlineKeyboardButton("🔍 Change Filter", callback_data="logs_filter")
        ],
        [
            InlineKeyboardButton("◀️ Back to Logs", callback_data="logs_menu")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


# Command handler
async def logs_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /logs command"""
    await show_logs_menu(update, context)
