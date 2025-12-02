"""
Scripts Execution Handlers

Handles custom bash script execution via inline keyboard.
Full button-based interface - no typing required!
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from ..modules.scripts.manager import ScriptsManager


# Initialize scripts manager
scripts_manager = ScriptsManager()


async def scripts_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /scripts command - show Scripts main menu"""
    await show_scripts_menu(update, context)


async def show_scripts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show main Scripts menu with inline keyboard"""
    query = update.callback_query
    
    text = (
        "📜 <b>Custom Scripts</b>\n\n"
        "Execute preset bash scripts for common tasks.\n"
        "Select a category:"
    )
    
    categories = scripts_manager.get_categories()
    
    keyboard = []
    for cat_id, cat_name in categories.items():
        keyboard.append([InlineKeyboardButton(cat_name, callback_data=f"script_cat_{cat_id}")])
    
    keyboard.extend([
        [InlineKeyboardButton("📜 History", callback_data="script_history")],
        [InlineKeyboardButton("🔙 Back to Tools", callback_data="menu_tools")]
    ])
    
    if query:
        await query.answer()
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
    else:
        await update.message.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )


async def show_category_scripts(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str) -> None:
    """Show scripts in a category"""
    query = update.callback_query
    await query.answer()
    
    categories = scripts_manager.get_categories()
    category_name = categories.get(category, 'Scripts')
    
    scripts = scripts_manager.get_scripts_by_category(category)
    
    text = f"<b>{category_name}</b>\n\nSelect a script to execute:"
    
    keyboard = []
    for script_id, script_info in scripts.items():
        keyboard.append([
            InlineKeyboardButton(
                script_info['name'],
                callback_data=f"script_info_{category}_{script_id}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="menu_scripts")])
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def show_script_info(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str, script_id: str) -> None:
    """Show script information and execution option"""
    query = update.callback_query
    await query.answer()
    
    script = scripts_manager.get_script(category, script_id)
    
    if not script:
        text = "❌ Script not found."
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu_scripts")]]
    else:
        text = (
            f"📜 <b>{script['name']}</b>\n\n"
            f"<b>Description:</b>\n{script['description']}\n\n"
            f"<b>Script Preview:</b>\n"
            f"<code>{script['script'][:200]}...</code>"
        )
        
        keyboard = [
            [InlineKeyboardButton("▶️ Execute Script", callback_data=f"script_exec_{category}_{script_id}_confirm")],
            [InlineKeyboardButton("🔙 Back", callback_data=f"script_cat_{category}")]
        ]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def confirm_script_execution(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str, script_id: str) -> None:
    """Show confirmation dialog for script execution"""
    query = update.callback_query
    await query.answer()
    
    script = scripts_manager.get_script(category, script_id)
    
    if not script:
        text = "❌ Script not found."
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu_scripts")]]
    else:
        text = (
            f"⚠️ <b>Execute Script</b>\n\n"
            f"Script: <b>{script['name']}</b>\n\n"
            f"This will execute the script on your system.\n"
            f"Are you sure?"
        )
        
        keyboard = [
            [
                InlineKeyboardButton("✅ Execute", callback_data=f"script_exec_{category}_{script_id}"),
                InlineKeyboardButton("❌ Cancel", callback_data=f"script_info_{category}_{script_id}")
            ]
        ]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def execute_script(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str, script_id: str) -> None:
    """Execute a script"""
    query = update.callback_query
    await query.answer()
    
    script = scripts_manager.get_script(category, script_id)
    
    if not script:
        text = "❌ Script not found."
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu_scripts")]]
        
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
        return
    
    # Show executing message
    await query.edit_message_text(
        f"⏳ Executing <b>{script['name']}</b>...\n\nPlease wait...",
        parse_mode=ParseMode.HTML
    )
    
    # Execute script
    success, stdout, stderr = scripts_manager.execute_script(script['script'], timeout=30)
    
    # Prepare output
    output = stdout if stdout else stderr
    
    # Save to history
    scripts_manager.save_to_history(
        script['name'],
        category,
        success,
        output
    )
    
    # Format result
    icon = "✅" if success else "❌"
    status = "Success" if success else "Failed"
    
    text = (
        f"{icon} <b>{script['name']}</b>\n"
        f"Status: {status}\n\n"
        f"<b>Output:</b>\n"
        f"{scripts_manager.format_output(output, max_length=2500)}"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔄 Run Again", callback_data=f"script_exec_{category}_{script_id}_confirm")],
        [InlineKeyboardButton("🔙 Back to Category", callback_data=f"script_cat_{category}")]
    ]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def show_script_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show script execution history"""
    query = update.callback_query
    await query.answer()
    
    history = scripts_manager.get_history(limit=10)
    text = scripts_manager.format_history(history)
    
    keyboard = []
    
    if history:
        keyboard.append([InlineKeyboardButton("🗑️ Clear History", callback_data="script_clear_history_confirm")])
    
    keyboard.extend([
        [InlineKeyboardButton("🔄 Refresh", callback_data="script_history")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu_scripts")]
    ])
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def confirm_clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show confirmation for clearing history"""
    query = update.callback_query
    await query.answer()
    
    text = (
        "🗑️ <b>Clear History</b>\n\n"
        "Are you sure you want to clear all script execution history?\n"
        "This action cannot be undone."
    )
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Clear", callback_data="script_clear_history"),
            InlineKeyboardButton("❌ Cancel", callback_data="script_history")
        ]
    ]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def clear_script_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear script execution history"""
    query = update.callback_query
    await query.answer()
    
    success = scripts_manager.clear_history()
    
    if success:
        text = "✅ Script history cleared successfully!"
    else:
        text = "❌ Failed to clear history."
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu_scripts")]]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )
