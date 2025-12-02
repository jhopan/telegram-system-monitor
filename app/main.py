#!/usr/bin/env python3
"""
Bot Telegram Monitoring Sistem Linux/Debian
Main Application Entry Point

Author: Your Name
Version: 2.0
"""

import sys
import logging
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
)
from config.settings import config, setup_logging

# Import handlers
from src.handlers.basic_handlers import (
    start_command,
    help_command,
    menu_command,
    admin_info_command
)
from src.handlers.system_handlers import (
    system_command,
    cpu_command,
    memory_command,
    uptime_command,
    processes_command,
    users_command
)
from src.handlers.disk_handlers import (
    disk_command,
    partitions_command,
    diskio_command
)
from src.handlers.network_handlers import (
    network_command,
    netstats_command,
    connections_command,
    publicip_command,
    ping_command,
    route_command,
    dns_command
)
from src.handlers.service_handlers import (
    services_command,
    services_running_command,
    services_failed_command,
    service_status_command,
    service_logs_command,
    service_start_command,
    service_stop_command,
    service_restart_command
)
from src.handlers.device_handlers import (
    device_command,
    sensors_command,
    battery_command
)
from src.handlers.chart_handlers import (
    chart_cpu_command,
    chart_memory_command,
    chart_disk_command,
    chart_network_command,
    charts_menu_command
)
from src.handlers.alert_handlers import (
    alerts_menu_command
)
from src.handlers.report_handlers import (
    reports_menu_command
)
from src.handlers.process_handlers import (
    processes_menu_command
)
from src.handlers.docker_handlers import (
    docker_menu_command
)
from src.handlers.package_handlers import (
    packages_menu_command
)
from src.handlers.callback_handler import button_handler
from src.modules.scheduler import BackgroundScheduler

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


def register_handlers(application: Application):
    """Register all command handlers"""
    
    # Basic commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("admininfo", admin_info_command))
    
    # System commands
    application.add_handler(CommandHandler("system", system_command))
    application.add_handler(CommandHandler("cpu", cpu_command))
    application.add_handler(CommandHandler("memory", memory_command))
    application.add_handler(CommandHandler("uptime", uptime_command))
    application.add_handler(CommandHandler("processes", processes_command))
    application.add_handler(CommandHandler("users", users_command))
    
    # Disk commands
    application.add_handler(CommandHandler("disk", disk_command))
    application.add_handler(CommandHandler("partitions", partitions_command))
    application.add_handler(CommandHandler("diskio", diskio_command))
    
    # Network commands
    application.add_handler(CommandHandler("network", network_command))
    application.add_handler(CommandHandler("netstats", netstats_command))
    application.add_handler(CommandHandler("connections", connections_command))
    application.add_handler(CommandHandler("publicip", publicip_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(CommandHandler("route", route_command))
    application.add_handler(CommandHandler("dns", dns_command))
    
    # Service commands
    application.add_handler(CommandHandler("services", services_command))
    application.add_handler(CommandHandler("services_running", services_running_command))
    application.add_handler(CommandHandler("services_failed", services_failed_command))
    application.add_handler(CommandHandler("service_status", service_status_command))
    application.add_handler(CommandHandler("service_logs", service_logs_command))
    application.add_handler(CommandHandler("service_start", service_start_command))
    application.add_handler(CommandHandler("service_stop", service_stop_command))
    application.add_handler(CommandHandler("service_restart", service_restart_command))
    
    # Device commands
    application.add_handler(CommandHandler("device", device_command))
    application.add_handler(CommandHandler("sensors", sensors_command))
    application.add_handler(CommandHandler("battery", battery_command))
    
    # Chart commands
    application.add_handler(CommandHandler("chart_cpu", chart_cpu_command))
    application.add_handler(CommandHandler("chart_memory", chart_memory_command))
    application.add_handler(CommandHandler("chart_disk", chart_disk_command))
    application.add_handler(CommandHandler("chart_network", chart_network_command))
    application.add_handler(CommandHandler("charts", charts_menu_command))
    
    # Alert commands
    application.add_handler(CommandHandler("alerts", alerts_menu_command))
    
    # Report commands
    application.add_handler(CommandHandler("reports", reports_menu_command))
    
    # Process commands
    application.add_handler(CommandHandler("processes", processes_menu_command))
    
    # Docker commands
    application.add_handler(CommandHandler("docker", docker_menu_command))
    
    # Package commands
    application.add_handler(CommandHandler("packages", packages_menu_command))
    
    # Callback query handler (inline keyboards)
    application.add_handler(CallbackQueryHandler(button_handler))
    
    logger.info("All handlers registered successfully")


async def error_handler(update, context):
    """Log errors"""
    logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)


def main():
    """Main function"""
    logger.info("=" * 50)
    logger.info("Starting Telegram System Monitor Bot")
    logger.info("=" * 50)
    
    # Show configuration
    logger.info(f"Bot Token: {'*' * 10}{config.TOKEN[-10:]}")
    logger.info(f"Authentication: {'Enabled' if config.ENABLE_AUTH else 'Disabled'}")
    logger.info(f"Admin User IDs: {len(config.ADMIN_USER_IDS)}")
    logger.info(f"Admin Usernames: {len(config.ADMIN_USERNAMES)}")
    logger.info(f"Service Control: {'Enabled' if config.ENABLE_SERVICE_CONTROL else 'Disabled'}")
    
    if config.ENABLE_AUTH:
        if config.ADMIN_USER_IDS:
            logger.info(f"  Authorized User IDs: {config.ADMIN_USER_IDS}")
        if config.ADMIN_USERNAMES:
            logger.info(f"  Authorized Usernames: {config.ADMIN_USERNAMES}")
    else:
        logger.warning("⚠️  Authentication is DISABLED! Anyone can use this bot!")
    
    logger.info("=" * 50)
    
    try:
        # Create application
        application = Application.builder().token(config.TOKEN).build()
        
        # Register all handlers
        register_handlers(application)
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        # Initialize and start background scheduler
        scheduler = BackgroundScheduler(application)
        scheduler.start(interval_minutes=5)  # Check every 5 minutes
        logger.info("Background scheduler initialized")
        
        # Start bot
        logger.info("Bot started successfully! Press Ctrl+C to stop.")
        logger.info("=" * 50)
        
        application.run_polling(allowed_updates=['message', 'callback_query'])
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        if 'scheduler' in locals():
            scheduler.stop()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        if 'scheduler' in locals():
            scheduler.stop()
        sys.exit(1)


if __name__ == '__main__':
    main()
