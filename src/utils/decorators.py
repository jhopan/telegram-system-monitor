"""
Authorization Decorator
"""
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from config.settings import config
import logging

logger = logging.getLogger(__name__)


def require_admin(func):
    """
    Decorator untuk memastikan hanya admin yang bisa akses command
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        user_id = user.id
        username = user.username
        
        # Check authorization
        if not config.is_admin(user_id, username):
            logger.warning(
                f"Unauthorized access attempt by user {user_id} "
                f"(@{username}) - {user.full_name}"
            )
            await update.message.reply_text(
                "❌ *Access Denied*\n\n"
                "Anda tidak memiliki akses ke bot ini.\n"
                "Hubungi administrator untuk mendapatkan akses.",
                parse_mode='Markdown'
            )
            return
        
        # User is authorized, proceed with command
        logger.info(
            f"Authorized command from user {user_id} "
            f"(@{username}) - {user.full_name}: {update.message.text}"
        )
        return await func(update, context, *args, **kwargs)
    
    return wrapper


def require_admin_callback(func):
    """
    Decorator untuk callback query (inline keyboard)
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        user_id = user.id
        username = user.username
        
        # Check authorization
        if not config.is_admin(user_id, username):
            logger.warning(
                f"Unauthorized callback query by user {user_id} "
                f"(@{username}) - {user.full_name}"
            )
            await update.callback_query.answer(
                "❌ Access Denied",
                show_alert=True
            )
            return
        
        # User is authorized, proceed
        return await func(update, context, *args, **kwargs)
    
    return wrapper
