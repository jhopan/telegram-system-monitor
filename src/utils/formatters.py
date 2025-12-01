"""
Utility Functions - Formatters
"""
from datetime import timedelta


def format_bytes(bytes_value: int, suffix: str = "B") -> str:
    """
    Scale bytes to its proper format
    e.g: 1253656 => '1.20MB'
    
    Args:
        bytes_value: Number of bytes
        suffix: Suffix untuk unit (default: "B")
    
    Returns:
        Formatted string
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes_value < factor:
            return f"{bytes_value:.2f}{unit}{suffix}"
        bytes_value /= factor
    return f"{bytes_value:.2f}P{suffix}"


def format_timedelta(td: timedelta) -> str:
    """
    Format timedelta ke string yang readable
    
    Args:
        td: timedelta object
    
    Returns:
        Formatted string (e.g., "2 hari, 3 jam, 45 menit")
    """
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days} hari")
    if hours > 0:
        parts.append(f"{hours} jam")
    if minutes > 0:
        parts.append(f"{minutes} menit")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} detik")
    
    return ", ".join(parts)


def format_number(number: int) -> str:
    """
    Format number dengan thousand separator
    
    Args:
        number: Number to format
    
    Returns:
        Formatted string (e.g., "1,234,567")
    """
    return f"{number:,}"


def truncate_message(message: str, max_length: int = 4000) -> list:
    """
    Split message jika terlalu panjang untuk Telegram
    
    Args:
        message: Message to split
        max_length: Maximum length per chunk
    
    Returns:
        List of message chunks
    """
    if len(message) <= max_length:
        return [message]
    
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
    
    return chunks
