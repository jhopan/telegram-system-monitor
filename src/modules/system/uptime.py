"""
System Uptime Module
"""
import psutil
from datetime import datetime
from src.utils.formatters import format_timedelta


def get_uptime() -> str:
    """Informasi uptime sistem"""
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime_duration = datetime.now() - boot_time
    
    info = f"⏰ *UPTIME SISTEM*\n\n"
    info += f"*Boot Time:* {boot_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    info += f"*Uptime:* {format_timedelta(uptime_duration)}\n"
    
    return info
