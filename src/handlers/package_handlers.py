"""
Package Management Handlers

Handles APT package management via inline keyboard.
Full button-based interface - no typing required!
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from ..modules.packages.manager import PackageManager


# Initialize package manager
package_manager = PackageManager()


async def packages_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /packages command - show Package main menu"""
    await show_packages_menu(update, context)


async def show_packages_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show main Package management menu with inline keyboard"""
    query = update.callback_query
    
    if not package_manager.apt_available:
        text = (
            "❌ <b>APT Not Available</b>\n\n"
            "APT package manager is not available on this system.\n"
            "This feature requires Debian/Ubuntu-based Linux."
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
    
    # Get package stats
    stats = package_manager.get_package_count()
    
    text = (
        f"📦 <b>Package Management</b>\n\n"
        f"Installed: {stats['installed']} packages\n"
        f"Upgradeable: {stats['upgradeable']} packages\n\n"
        f"Select an option below:"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("📋 Installed", callback_data="pkg_installed"),
            InlineKeyboardButton("⬆️ Upgradeable", callback_data="pkg_upgradeable")
        ],
        [
            InlineKeyboardButton("🔍 Search by Category", callback_data="pkg_categories")
        ],
        [
            InlineKeyboardButton("🔄 Update List", callback_data="pkg_update"),
            InlineKeyboardButton("⬆️ Upgrade All", callback_data="pkg_upgrade_all")
        ],
        [
            InlineKeyboardButton("🗑️ Autoremove", callback_data="pkg_autoremove")
        ],
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


async def show_installed_packages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show list of installed packages"""
    query = update.callback_query
    await query.answer("Loading installed packages...")
    
    packages = package_manager.get_installed_packages(limit=20)
    text = package_manager.format_package_list(packages, "Installed Packages")
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data="pkg_installed")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu_packages")]
    ]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def show_upgradeable_packages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show list of upgradeable packages"""
    query = update.callback_query
    await query.answer("Checking for updates...")
    
    packages = package_manager.get_upgradeable_packages()
    
    if not packages:
        text = "✅ <b>All packages are up to date!</b>\n\nNo upgrades available."
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu_packages")]]
    else:
        text = package_manager.format_package_list(packages, "Upgradeable Packages")
        keyboard = [
            [InlineKeyboardButton("⬆️ Upgrade All Now", callback_data="pkg_upgrade_all_confirm")],
            [InlineKeyboardButton("🔙 Back", callback_data="menu_packages")]
        ]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def show_package_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show package categories"""
    query = update.callback_query
    await query.answer()
    
    text = (
        "🔍 <b>Package Categories</b>\n\n"
        "Browse and install packages by category:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🌐 Web Servers", callback_data="pkg_cat_webserver")],
        [InlineKeyboardButton("🗄️ Databases", callback_data="pkg_cat_database")],
        [InlineKeyboardButton("⚙️ Development Tools", callback_data="pkg_cat_devtools")],
        [InlineKeyboardButton("📊 Monitoring Tools", callback_data="pkg_cat_monitoring")],
        [InlineKeyboardButton("🛡️ System & Security", callback_data="pkg_cat_system")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu_packages")]
    ]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def show_category_packages(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str) -> None:
    """Show packages in a category"""
    query = update.callback_query
    await query.answer()
    
    category_names = {
        'webserver': '🌐 Web Servers',
        'database': '🗄️ Databases',
        'devtools': '⚙️ Development Tools',
        'monitoring': '📊 Monitoring Tools',
        'system': '🛡️ System & Security'
    }
    
    packages = package_manager.get_preset_packages(category)
    
    text = f"<b>{category_names.get(category, 'Packages')}</b>\n\n"
    
    keyboard = []
    for pkg_name, description in packages.items():
        installed = package_manager.is_package_installed(pkg_name)
        icon = "✅" if installed else "📦"
        keyboard.append([
            InlineKeyboardButton(
                f"{icon} {pkg_name}",
                callback_data=f"pkg_info_{category}_{pkg_name}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="pkg_categories")])
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def show_package_info(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str, package_name: str) -> None:
    """Show detailed package information"""
    query = update.callback_query
    await query.answer("Loading package info...")
    
    info = package_manager.get_package_info(package_name)
    installed = package_manager.is_package_installed(package_name)
    
    if info:
        text = package_manager.format_package_info(info)
    else:
        text = f"📦 <b>{package_name}</b>\n\nPackage information not available."
    
    keyboard = []
    
    if installed:
        keyboard.append([
            InlineKeyboardButton("🗑️ Remove", callback_data=f"pkg_remove_{package_name}_confirm")
        ])
    else:
        keyboard.append([
            InlineKeyboardButton("📥 Install", callback_data=f"pkg_install_{package_name}_confirm")
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=f"pkg_cat_{category}")])
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def handle_package_action(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    action: str,
    package_name: Optional[str] = None
) -> None:
    """Handle package actions (install, remove, update, upgrade, autoremove)"""
    query = update.callback_query
    await query.answer()
    
    # Show processing message
    if action == 'update':
        processing_text = "🔄 Updating package list...\nThis may take a minute..."
    elif action == 'upgrade_all':
        processing_text = "⬆️ Upgrading all packages...\nThis may take several minutes..."
    elif action == 'install':
        processing_text = f"📥 Installing {package_name}...\nPlease wait..."
    elif action == 'remove':
        processing_text = f"🗑️ Removing {package_name}...\nPlease wait..."
    elif action == 'autoremove':
        processing_text = "🗑️ Removing unused packages...\nPlease wait..."
    else:
        processing_text = "Processing..."
    
    await query.edit_message_text(
        text=processing_text,
        parse_mode=ParseMode.HTML
    )
    
    # Execute action
    success = False
    message = ""
    
    if action == 'update':
        success, message = package_manager.update_package_list()
    elif action == 'upgrade_all':
        success, message = package_manager.upgrade_packages()
    elif action == 'install' and package_name:
        success, message = package_manager.install_package(package_name)
    elif action == 'remove' and package_name:
        success, message = package_manager.remove_package(package_name)
    elif action == 'autoremove':
        success, message = package_manager.autoremove()
    
    # Show result
    if success:
        icon = "✅"
    else:
        icon = "❌"
    
    text = f"{icon} <b>Package Manager</b>\n\n{message}"
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Packages", callback_data="menu_packages")]]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )


async def confirm_action(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    action: str,
    package_name: str
) -> None:
    """Show confirmation dialog for package actions"""
    query = update.callback_query
    await query.answer()
    
    if action == 'install':
        text = (
            f"📥 <b>Install Package</b>\n\n"
            f"Package: <code>{package_name}</code>\n\n"
            f"Are you sure you want to install this package?"
        )
        confirm_callback = f"pkg_install_{package_name}"
    elif action == 'remove':
        text = (
            f"🗑️ <b>Remove Package</b>\n\n"
            f"Package: <code>{package_name}</code>\n\n"
            f"⚠️ Are you sure you want to remove this package?"
        )
        confirm_callback = f"pkg_remove_{package_name}"
    elif action == 'upgrade_all':
        text = (
            f"⬆️ <b>Upgrade All Packages</b>\n\n"
            f"This will upgrade all upgradeable packages.\n\n"
            f"⚠️ This may take several minutes. Continue?"
        )
        confirm_callback = "pkg_upgrade_all"
    else:
        return
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Confirm", callback_data=confirm_callback),
            InlineKeyboardButton("❌ Cancel", callback_data="menu_packages")
        ]
    ]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )
