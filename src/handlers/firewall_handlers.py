"""
Firewall Management Handlers

Handles UFW firewall management via inline keyboard.
Full button-based interface - no typing required!
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from ..modules.firewall.manager import FirewallManager


# Initialize firewall manager
firewall_manager = FirewallManager()


async def firewall_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /firewall command - show Firewall main menu"""
    await show_firewall_menu(update, context)


async def show_firewall_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show main Firewall management menu with inline keyboard"""
    query = update.callback_query
    
    if not firewall_manager.ufw_available:
        text = (
            "❌ <b>UFW Not Available</b>\n\n"
            "UFW (Uncomplicated Firewall) is not installed on this system.\n"
            "Install it with: <code>apt install ufw</code>"
        )
        keyboard = [[InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]]
        
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
    
    # Get firewall status
    status = firewall_manager.get_status()
    text = firewall_manager.format_status(status)
    
    enabled = status.get('enabled', False)
    
    keyboard = []
    
    # Enable/Disable toggle
    if enabled:
        keyboard.append([InlineKeyboardButton("🔴 Disable Firewall", callback_data="fw_disable_confirm")])
    else:
        keyboard.append([InlineKeyboardButton("🟢 Enable Firewall", callback_data="fw_enable")])
    
    keyboard.extend([
        [
            InlineKeyboardButton("📋 View Rules", callback_data="fw_rules"),
            InlineKeyboardButton("➕ Add Rule", callback_data="fw_add_menu")
        ],
        [
            InlineKeyboardButton("⚙️ Default Policies", callback_data="fw_policies"),
            InlineKeyboardButton("🔄 Reset", callback_data="fw_reset_confirm")
        ],
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


async def show_firewall_rules(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show list of firewall rules"""
    query = update.callback_query
    await query.answer("Loading rules...")
    
    rules = firewall_manager.get_rules()
    text = firewall_manager.format_rules(rules)
    
    keyboard = []
    
    # Add delete buttons for each rule
    if rules:
        for rule in rules[:10]:  # Limit to 10 rules
            keyboard.append([
                InlineKeyboardButton(
                    f"🗑️ Delete Rule #{rule['number']} ({rule['port_proto']})",
                    callback_data=f"fw_delete_{rule['number']}_confirm"
                )
            ])
    
    keyboard.extend([
        [InlineKeyboardButton("🔄 Refresh", callback_data="fw_rules")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu_firewall")]
    ])
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def show_add_rule_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show menu for adding firewall rules"""
    query = update.callback_query
    await query.answer()
    
    text = (
        "➕ <b>Add Firewall Rule</b>\n\n"
        "Select a service to allow:"
    )
    
    services = firewall_manager.get_preset_services()
    
    keyboard = []
    
    # Group services
    common = [
        ('ssh', '🔐 SSH (22)'),
        ('http', '🌐 HTTP (80)'),
        ('https', '🔒 HTTPS (443)')
    ]
    
    databases = [
        ('mysql', '🗄️ MySQL (3306)'),
        ('postgresql', '🐘 PostgreSQL (5432)'),
        ('mongodb', '🍃 MongoDB (27017)'),
        ('redis', '📦 Redis (6379)')
    ]
    
    other = [
        ('ftp', '📁 FTP (21)'),
        ('smtp', '📧 SMTP (25)'),
        ('dns', '🌐 DNS (53)'),
        ('docker', '🐳 Docker (2375)')
    ]
    
    # Add common services
    for key, label in common:
        keyboard.append([InlineKeyboardButton(label, callback_data=f"fw_add_{key}")])
    
    # Add databases
    keyboard.append([InlineKeyboardButton("🗄️ Databases ↓", callback_data="fw_add_db_menu")])
    
    # Add other services
    keyboard.append([InlineKeyboardButton("⚙️ Other Services ↓", callback_data="fw_add_other_menu")])
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="menu_firewall")])
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def show_database_services(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show database services for firewall rules"""
    query = update.callback_query
    await query.answer()
    
    text = "🗄️ <b>Database Services</b>\n\nSelect a database service:"
    
    keyboard = [
        [InlineKeyboardButton("🗄️ MySQL (3306)", callback_data="fw_add_mysql")],
        [InlineKeyboardButton("🐘 PostgreSQL (5432)", callback_data="fw_add_postgresql")],
        [InlineKeyboardButton("🍃 MongoDB (27017)", callback_data="fw_add_mongodb")],
        [InlineKeyboardButton("📦 Redis (6379)", callback_data="fw_add_redis")],
        [InlineKeyboardButton("🔙 Back", callback_data="fw_add_menu")]
    ]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def show_other_services(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show other services for firewall rules"""
    query = update.callback_query
    await query.answer()
    
    text = "⚙️ <b>Other Services</b>\n\nSelect a service:"
    
    keyboard = [
        [InlineKeyboardButton("📁 FTP (21)", callback_data="fw_add_ftp")],
        [InlineKeyboardButton("📧 SMTP (25)", callback_data="fw_add_smtp")],
        [InlineKeyboardButton("🌐 DNS (53 UDP)", callback_data="fw_add_dns")],
        [InlineKeyboardButton("🐳 Docker (2375)", callback_data="fw_add_docker")],
        [InlineKeyboardButton("🔙 Back", callback_data="fw_add_menu")]
    ]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def show_default_policies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show default policies menu"""
    query = update.callback_query
    await query.answer()
    
    status = firewall_manager.get_status()
    
    text = (
        "⚙️ <b>Default Policies</b>\n\n"
        f"Current settings:\n"
        f"• Incoming: <code>{status.get('default_incoming', 'unknown')}</code>\n"
        f"• Outgoing: <code>{status.get('default_outgoing', 'unknown')}</code>\n\n"
        f"Select a policy to change:"
    )
    
    keyboard = [
        [InlineKeyboardButton("⬇️ Incoming Policy", callback_data="fw_policy_incoming")],
        [InlineKeyboardButton("⬆️ Outgoing Policy", callback_data="fw_policy_outgoing")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu_firewall")]
    ]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def show_policy_options(update: Update, context: ContextTypes.DEFAULT_TYPE, direction: str) -> None:
    """Show policy options for a direction"""
    query = update.callback_query
    await query.answer()
    
    direction_text = "Incoming" if direction == "incoming" else "Outgoing"
    icon = "⬇️" if direction == "incoming" else "⬆️"
    
    text = f"{icon} <b>{direction_text} Policy</b>\n\nSelect default policy:"
    
    keyboard = [
        [InlineKeyboardButton("🔒 Deny (Recommended)", callback_data=f"fw_setpolicy_{direction}_deny")],
        [InlineKeyboardButton("🔓 Allow", callback_data=f"fw_setpolicy_{direction}_allow")],
        [InlineKeyboardButton("❌ Reject", callback_data=f"fw_setpolicy_{direction}_reject")],
        [InlineKeyboardButton("🔙 Back", callback_data="fw_policies")]
    ]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def handle_firewall_action(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    action: str,
    value: Optional[str] = None
) -> None:
    """Handle firewall actions"""
    query = update.callback_query
    await query.answer()
    
    success = False
    message = ""
    
    if action == 'enable':
        await query.edit_message_text("🟢 Enabling firewall...", parse_mode=ParseMode.HTML)
        success, message = firewall_manager.enable()
    
    elif action == 'disable':
        await query.edit_message_text("🔴 Disabling firewall...", parse_mode=ParseMode.HTML)
        success, message = firewall_manager.disable()
    
    elif action == 'reset':
        await query.edit_message_text("🔄 Resetting firewall...", parse_mode=ParseMode.HTML)
        success, message = firewall_manager.reset()
    
    elif action == 'add_rule' and value:
        services = firewall_manager.get_preset_services()
        if value in services:
            service = services[value]
            await query.edit_message_text(
                f"➕ Adding rule for {service['name']}...",
                parse_mode=ParseMode.HTML
            )
            success, message = firewall_manager.add_rule(
                service['port'],
                service['protocol']
            )
    
    elif action == 'delete_rule' and value:
        await query.edit_message_text(f"🗑️ Deleting rule #{value}...", parse_mode=ParseMode.HTML)
        success, message = firewall_manager.delete_rule(value)
    
    elif action == 'set_policy' and value:
        parts = value.split('_')
        if len(parts) == 2:
            direction, policy = parts
            await query.edit_message_text(
                f"⚙️ Setting {direction} policy to {policy}...",
                parse_mode=ParseMode.HTML
            )
            success, message = firewall_manager.set_default_policy(direction, policy)
    
    # Show result
    icon = "✅" if success else "❌"
    text = f"{icon} <b>Firewall</b>\n\n{message}"
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Firewall", callback_data="menu_firewall")]]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def confirm_firewall_action(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    action: str,
    value: Optional[str] = None
) -> None:
    """Show confirmation dialog for firewall actions"""
    query = update.callback_query
    await query.answer()
    
    if action == 'disable':
        text = (
            "🔴 <b>Disable Firewall</b>\n\n"
            "⚠️ This will disable all firewall protection.\n"
            "Your system will be exposed to the network.\n\n"
            "Are you sure?"
        )
        confirm_callback = "fw_disable"
    
    elif action == 'reset':
        text = (
            "🔄 <b>Reset Firewall</b>\n\n"
            "⚠️ This will delete ALL rules and reset to defaults.\n"
            "This action cannot be undone.\n\n"
            "Are you sure?"
        )
        confirm_callback = "fw_reset"
    
    elif action == 'delete_rule' and value:
        rules = firewall_manager.get_rules()
        rule = next((r for r in rules if r['number'] == value), None)
        rule_info = f"{rule['port_proto']} - {rule['action']}" if rule else f"Rule #{value}"
        
        text = (
            f"🗑️ <b>Delete Rule</b>\n\n"
            f"Rule: <code>{rule_info}</code>\n\n"
            f"Are you sure you want to delete this rule?"
        )
        confirm_callback = f"fw_delete_{value}"
    
    else:
        return
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Confirm", callback_data=confirm_callback),
            InlineKeyboardButton("❌ Cancel", callback_data="menu_firewall")
        ]
    ]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )
