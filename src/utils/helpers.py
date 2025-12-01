"""
Message Helper Functions
"""
from telegram import Update
from telegram.constants import ParseMode
from config.settings import config


async def send_long_message(update: Update, message: str, parse_mode: str = ParseMode.MARKDOWN):
    """
    Send message yang mungkin terlalu panjang, auto-split jika perlu
    
    Args:
        update: Telegram update object
        message: Message to send
        parse_mode: Parse mode (Markdown or HTML)
    """
    max_length = config.MAX_MESSAGE_LENGTH
    
    if len(message) <= max_length:
        await update.message.reply_text(message, parse_mode=parse_mode)
        return
    
    # Split message into chunks
    chunks = []
    current_chunk = ""
    
    for line in message.split('\n'):
        if len(current_chunk) + len(line) + 1 > max_length:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = line + '\n'
        else:
            current_chunk += line + '\n'
    
    if current_chunk:
        chunks.append(current_chunk)
    
    # Send all chunks
    for chunk in chunks:
        await update.message.reply_text(chunk, parse_mode=parse_mode)


async def send_error_message(update: Update, error_text: str):
    """
    Send formatted error message
    
    Args:
        update: Telegram update object
        error_text: Error message
    """
    message = f"❌ *Error*\n\n{error_text}"
    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


async def send_success_message(update: Update, success_text: str):
    """
    Send formatted success message
    
    Args:
        update: Telegram update object
        success_text: Success message
    """
    message = f"✅ *Success*\n\n{success_text}"
    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
