"""
Process Handlers
Advanced process management via inline keyboard
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from src.utils.decorators import require_admin
from src.modules.process import ProcessManager
import json

# Conversation states
SEARCH_INPUT, KILL_CONFIRM, NICE_INPUT = range(3)

# Initialize manager
process_manager = ProcessManager()


@require_admin
async def processes_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show process manager menu"""
    text = """
🔧 *PROCESS MANAGER*

Advanced process management tools
"""
    keyboard = [
        [
            InlineKeyboardButton("📊 Top CPU", callback_data='proc_top_cpu'),
            InlineKeyboardButton("🧠 Top Memory", callback_data='proc_top_memory')
        ],
        [
            InlineKeyboardButton("🔍 Search", callback_data='proc_search_menu'),
            InlineKeyboardButton("🗂️ Filter", callback_data='proc_filter_menu')
        ],
        [
            InlineKeyboardButton("📋 All Processes", callback_data='proc_all'),
            InlineKeyboardButton("🔄 Refresh", callback_data='proc_refresh')
        ],
        [InlineKeyboardButton("◀️ Back to Main", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def show_processes_menu(query):
    """Show process manager menu"""
    text = """
🔧 *PROCESS MANAGER*

Advanced process management tools
"""
    keyboard = [
        [
            InlineKeyboardButton("📊 Top CPU", callback_data='proc_top_cpu'),
            InlineKeyboardButton("🧠 Top Memory", callback_data='proc_top_memory')
        ],
        [
            InlineKeyboardButton("🔍 Search", callback_data='proc_search_menu'),
            InlineKeyboardButton("🗂️ Filter", callback_data='proc_filter_menu')
        ],
        [
            InlineKeyboardButton("📋 All Processes", callback_data='proc_all'),
            InlineKeyboardButton("🔄 Refresh", callback_data='menu_processes')
        ],
        [InlineKeyboardButton("◀️ Back to Main", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def show_top_processes(query, sort_by='cpu'):
    """Show top processes"""
    await query.edit_message_text("⏳ Loading processes...")
    
    try:
        processes = process_manager.get_all_processes(sort_by=sort_by, limit=15)
        
        if sort_by == 'cpu':
            title = "📊 TOP CPU PROCESSES"
        elif sort_by == 'memory':
            title = "🧠 TOP MEMORY PROCESSES"
        else:
            title = "📋 ALL PROCESSES"
        
        text = process_manager.format_process_list(processes, title)
        
        # Create keyboard with process buttons
        keyboard = []
        for i, proc in enumerate(processes[:10]):  # Max 10 for buttons
            keyboard.append([
                InlineKeyboardButton(
                    f"{proc['name'][:20]} [{proc['pid']}]",
                    callback_data=f"proc_detail_{proc['pid']}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("◀️ Back", callback_data='menu_processes')])
        keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    except Exception as e:
        await query.edit_message_text(
            f"❌ Error loading processes: {str(e)}",
            parse_mode=ParseMode.MARKDOWN
        )


async def show_search_menu(query):
    """Show search options"""
    text = """
🔍 *SEARCH PROCESSES*

Quick search by common process names:
"""
    keyboard = [
        [
            InlineKeyboardButton("🐍 Python", callback_data='proc_search_python'),
            InlineKeyboardButton("🌐 Nginx", callback_data='proc_search_nginx')
        ],
        [
            InlineKeyboardButton("💾 MySQL", callback_data='proc_search_mysql'),
            InlineKeyboardButton("🐳 Docker", callback_data='proc_search_docker')
        ],
        [
            InlineKeyboardButton("📦 Apache", callback_data='proc_search_apache'),
            InlineKeyboardButton("⚡ Node", callback_data='proc_search_node')
        ],
        [
            InlineKeyboardButton("🔧 SSH", callback_data='proc_search_ssh'),
            InlineKeyboardButton("🖥️ Systemd", callback_data='proc_search_systemd')
        ],
        [InlineKeyboardButton("◀️ Back", callback_data='menu_processes')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def show_filter_menu(query):
    """Show filter options"""
    text = """
🗂️ *FILTER PROCESSES*

Filter by status or user:
"""
    keyboard = [
        [
            InlineKeyboardButton("🟢 Running", callback_data='proc_filter_running'),
            InlineKeyboardButton("🟡 Sleeping", callback_data='proc_filter_sleeping')
        ],
        [
            InlineKeyboardButton("🔴 Zombie", callback_data='proc_filter_zombie'),
            InlineKeyboardButton("⚫ Idle", callback_data='proc_filter_idle')
        ],
        [
            InlineKeyboardButton("👤 By User", callback_data='proc_filter_users')
        ],
        [InlineKeyboardButton("◀️ Back", callback_data='menu_processes')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def show_users_filter(query):
    """Show user filter options"""
    users = process_manager.get_users()
    
    text = """
👤 *FILTER BY USER*

Select user:
"""
    keyboard = []
    
    for i in range(0, len(users), 2):
        row = []
        row.append(InlineKeyboardButton(users[i], callback_data=f'proc_user_{users[i]}'))
        if i + 1 < len(users):
            row.append(InlineKeyboardButton(users[i + 1], callback_data=f'proc_user_{users[i + 1]}'))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("◀️ Back", callback_data='proc_filter_menu')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def search_processes(query, search_term):
    """Search and display processes"""
    await query.edit_message_text(f"🔍 Searching for '{search_term}'...")
    
    try:
        processes = process_manager.search_processes(search_term)
        
        title = f"🔍 SEARCH: {search_term.upper()}"
        text = process_manager.format_process_list(processes, title)
        
        # Create keyboard with process buttons
        keyboard = []
        for proc in processes[:10]:
            keyboard.append([
                InlineKeyboardButton(
                    f"{proc['name'][:20]} [{proc['pid']}]",
                    callback_data=f"proc_detail_{proc['pid']}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("◀️ Back", callback_data='proc_search_menu')])
        keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    except Exception as e:
        await query.edit_message_text(
            f"❌ Error: {str(e)}",
            parse_mode=ParseMode.MARKDOWN
        )


async def filter_processes(query, filter_type, filter_value):
    """Filter and display processes"""
    await query.edit_message_text(f"🗂️ Filtering by {filter_type}...")
    
    try:
        if filter_type == 'status':
            processes = process_manager.filter_by_status(filter_value)
            title = f"🗂️ STATUS: {filter_value.upper()}"
        elif filter_type == 'user':
            processes = process_manager.filter_by_user(filter_value)
            title = f"👤 USER: {filter_value}"
        else:
            processes = []
            title = "FILTERED PROCESSES"
        
        text = process_manager.format_process_list(processes, title)
        
        # Create keyboard with process buttons
        keyboard = []
        for proc in processes[:10]:
            keyboard.append([
                InlineKeyboardButton(
                    f"{proc['name'][:20]} [{proc['pid']}]",
                    callback_data=f"proc_detail_{proc['pid']}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("◀️ Back", callback_data='proc_filter_menu')])
        keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    except Exception as e:
        await query.edit_message_text(
            f"❌ Error: {str(e)}",
            parse_mode=ParseMode.MARKDOWN
        )


async def show_process_detail(query, pid):
    """Show detailed process info with action buttons"""
    await query.edit_message_text(f"⏳ Loading process {pid}...")
    
    try:
        info = process_manager.get_process_info(pid)
        
        if not info:
            await query.edit_message_text(
                f"❌ Process {pid} not found",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        text = process_manager.format_process_detail(info)
        
        # Action buttons
        keyboard = [
            [
                InlineKeyboardButton("🔴 Kill", callback_data=f'proc_kill_{pid}'),
                InlineKeyboardButton("⚡ Force Kill", callback_data=f'proc_forcekill_{pid}')
            ],
            [
                InlineKeyboardButton("⏸️ Suspend", callback_data=f'proc_suspend_{pid}'),
                InlineKeyboardButton("▶️ Resume", callback_data=f'proc_resume_{pid}')
            ],
            [
                InlineKeyboardButton("⬆️ Priority", callback_data=f'proc_priority_{pid}')
            ],
            [InlineKeyboardButton("🔄 Refresh", callback_data=f'proc_detail_{pid}')],
            [InlineKeyboardButton("◀️ Back", callback_data='menu_processes')],
            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    except Exception as e:
        await query.edit_message_text(
            f"❌ Error: {str(e)}",
            parse_mode=ParseMode.MARKDOWN
        )


async def show_priority_menu(query, pid):
    """Show priority change menu"""
    text = f"""
⬆️ *CHANGE PRIORITY*

PID: `{pid}`

Select nice value:
• -20: Highest priority
• 0: Normal priority
• 19: Lowest priority

_Lower value = Higher priority_
_Requires root for values < 0_
"""
    keyboard = [
        [
            InlineKeyboardButton("-20 (Highest)", callback_data=f'proc_nice_{pid}_-20'),
            InlineKeyboardButton("-10", callback_data=f'proc_nice_{pid}_-10')
        ],
        [
            InlineKeyboardButton("0 (Normal)", callback_data=f'proc_nice_{pid}_0'),
            InlineKeyboardButton("10", callback_data=f'proc_nice_{pid}_10')
        ],
        [
            InlineKeyboardButton("19 (Lowest)", callback_data=f'proc_nice_{pid}_19')
        ],
        [InlineKeyboardButton("◀️ Back", callback_data=f'proc_detail_{pid}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def handle_process_action(query, action, pid, value=None):
    """Handle process actions"""
    try:
        if action == 'kill':
            success, message = process_manager.kill_process(int(pid), force=False)
            icon = "✅" if success else "❌"
            
        elif action == 'forcekill':
            success, message = process_manager.kill_process(int(pid), force=True)
            icon = "✅" if success else "❌"
            
        elif action == 'suspend':
            success, message = process_manager.suspend_process(int(pid))
            icon = "✅" if success else "❌"
            
        elif action == 'resume':
            success, message = process_manager.resume_process(int(pid))
            icon = "✅" if success else "❌"
            
        elif action == 'nice':
            success, message = process_manager.change_priority(int(pid), int(value))
            icon = "✅" if success else "❌"
        
        else:
            success = False
            message = "Unknown action"
            icon = "❌"
        
        # Show result
        text = f"{icon} *PROCESS ACTION*\n\n{message}"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh Process", callback_data=f'proc_detail_{pid}')],
            [InlineKeyboardButton("◀️ Back to Manager", callback_data='menu_processes')],
            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
        
        await query.answer(message[:200])
    
    except Exception as e:
        await query.answer(f"❌ Error: {str(e)}")
