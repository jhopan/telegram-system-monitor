"""
Docker Handlers

Handles Docker monitoring and management commands via inline keyboard.
Full button-based interface - no typing required!
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from ..modules.docker.manager import DockerManager


# Initialize Docker manager
docker_manager = DockerManager()


async def docker_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /docker command - show Docker main menu"""
    await show_docker_menu(update, context)


async def show_docker_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show main Docker menu with inline keyboard"""
    query = update.callback_query
    
    if not docker_manager.docker_available:
        text = (
            "❌ <b>Docker Not Available</b>\n\n"
            "Docker is not installed or not running on this system.\n"
            "Please install Docker and ensure it's running."
        )
        keyboard = [[InlineKeyboardButton("🏠 Main Menu", callback_data="menu_main")]]
        
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
        return
    
    text = (
        "🐳 <b>Docker Management</b>\n\n"
        "Monitor and manage Docker containers.\n"
        "Select an option below:"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🟢 Running", callback_data="docker_running"),
            InlineKeyboardButton("🔴 Stopped", callback_data="docker_stopped")
        ],
        [InlineKeyboardButton("📋 All Containers", callback_data="docker_all")],
        [
            InlineKeyboardButton("▶️ Start All", callback_data="docker_start_all"),
            InlineKeyboardButton("⏹️ Stop All", callback_data="docker_stop_all")
        ],
        [InlineKeyboardButton("🗑️ Remove Stopped", callback_data="docker_remove_stopped")],
        [InlineKeyboardButton("🔙 Back to Tools", callback_data="menu_tools")]
    ]
    
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


async def show_containers(update: Update, context: ContextTypes.DEFAULT_TYPE, status: str = 'all') -> None:
    """Show list of containers"""
    query = update.callback_query
    await query.answer()
    
    containers = docker_manager.get_containers(status)
    
    if not containers:
        status_text = {
            'all': 'No containers',
            'running': 'No running containers',
            'stopped': 'No stopped containers'
        }.get(status, 'No containers')
        
        text = f"🐳 <b>Docker Containers</b>\n\n{status_text} found."
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu_docker")]]
        
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
        return
    
    text = docker_manager.format_container_list(containers)
    
    # Create buttons for each container
    keyboard = []
    for container in containers[:10]:  # Limit to 10 containers
        keyboard.append([
            InlineKeyboardButton(
                f"{container['name']} ({container['status']})",
                callback_data=f"docker_detail_{container['id']}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="menu_docker")])
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def show_container_detail(update: Update, context: ContextTypes.DEFAULT_TYPE, container_id: str) -> None:
    """Show detailed information about a container"""
    query = update.callback_query
    await query.answer()
    
    details = docker_manager.get_container_details(container_id)
    
    if not details:
        text = "❌ Container not found or error retrieving details."
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu_docker")]]
        
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
        return
    
    text = docker_manager.format_container_detail(details)
    
    # Action buttons based on container state
    keyboard = []
    
    if details['running']:
        keyboard.append([
            InlineKeyboardButton("⏹️ Stop", callback_data=f"docker_stop_{container_id}"),
            InlineKeyboardButton("🔄 Restart", callback_data=f"docker_restart_{container_id}")
        ])
    else:
        keyboard.append([
            InlineKeyboardButton("▶️ Start", callback_data=f"docker_start_{container_id}"),
            InlineKeyboardButton("🗑️ Remove", callback_data=f"docker_remove_{container_id}")
        ])
    
    keyboard.extend([
        [
            InlineKeyboardButton("📊 Stats", callback_data=f"docker_stats_{container_id}"),
            InlineKeyboardButton("📜 Logs", callback_data=f"docker_logs_{container_id}")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="docker_all")]
    ])
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def show_container_stats(update: Update, context: ContextTypes.DEFAULT_TYPE, container_id: str) -> None:
    """Show container statistics"""
    query = update.callback_query
    await query.answer()
    
    details = docker_manager.get_container_details(container_id)
    if not details:
        text = "❌ Container not found."
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu_docker")]]
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
        return
    
    stats = docker_manager.get_container_stats(container_id)
    
    if not stats:
        text = f"❌ Unable to retrieve stats for {details['name']}."
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data=f"docker_detail_{container_id}")]]
        
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
        return
    
    text = docker_manager.format_container_stats(stats, details['name'])
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data=f"docker_stats_{container_id}")],
        [InlineKeyboardButton("🔙 Back", callback_data=f"docker_detail_{container_id}")]
    ]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def show_container_logs(update: Update, context: ContextTypes.DEFAULT_TYPE, container_id: str) -> None:
    """Show container logs"""
    query = update.callback_query
    await query.answer()
    
    details = docker_manager.get_container_details(container_id)
    if not details:
        text = "❌ Container not found."
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu_docker")]]
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
        return
    
    logs = docker_manager.get_container_logs(container_id, lines=30)
    
    text = (
        f"📜 <b>Logs: {details['name']}</b>\n"
        f"<b>Last 30 lines</b>\n\n"
        f"<pre>{logs[:3000]}</pre>"  # Limit to 3000 chars
    )
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data=f"docker_logs_{container_id}")],
        [InlineKeyboardButton("🔙 Back", callback_data=f"docker_detail_{container_id}")]
    ]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def handle_container_action(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    action: str,
    container_id: str
) -> None:
    """Handle container actions (start, stop, restart, remove)"""
    query = update.callback_query
    await query.answer()
    
    # Get container name for better feedback
    details = docker_manager.get_container_details(container_id)
    container_name = details['name'] if details else container_id
    
    success = False
    action_text = ""
    
    if action == 'start':
        success = docker_manager.start_container(container_id)
        action_text = "started"
    elif action == 'stop':
        success = docker_manager.stop_container(container_id)
        action_text = "stopped"
    elif action == 'restart':
        success = docker_manager.restart_container(container_id)
        action_text = "restarted"
    elif action == 'remove':
        success = docker_manager.remove_container(container_id)
        action_text = "removed"
    
    if success:
        text = f"✅ Container <b>{container_name}</b> {action_text} successfully!"
        
        if action == 'remove':
            keyboard = [[InlineKeyboardButton("🔙 Back to Docker", callback_data="menu_docker")]]
        else:
            keyboard = [[InlineKeyboardButton("🔙 Back", callback_data=f"docker_detail_{container_id}")]]
    else:
        text = f"❌ Failed to {action} container <b>{container_name}</b>."
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data=f"docker_detail_{container_id}")]]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def handle_bulk_action(update: Update, context: ContextTypes.DEFAULT_TYPE, action: str) -> None:
    """Handle bulk actions (start all, stop all, remove stopped)"""
    query = update.callback_query
    await query.answer()
    
    count = 0
    action_text = ""
    
    if action == 'start_all':
        count = docker_manager.start_all_containers()
        action_text = "started"
    elif action == 'stop_all':
        count = docker_manager.stop_all_containers()
        action_text = "stopped"
    elif action == 'remove_stopped':
        count = docker_manager.remove_stopped_containers()
        action_text = "removed"
    
    if count > 0:
        text = f"✅ Successfully {action_text} {count} container(s)!"
    else:
        text = f"ℹ️ No containers to {action.replace('_', ' ')}."
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu_docker")]]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )
