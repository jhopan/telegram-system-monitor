"""
Users Information Module
"""
import psutil
from datetime import datetime


def get_users_info() -> str:
    """Informasi user yang login"""
    users = psutil.users()
    
    if not users:
        return "👥 *USER LOGIN*\n\nTidak ada user yang login saat ini."
    
    info = f"👥 *USER LOGIN*\n\n"
    for user in users:
        info += f"*User:* {user.name}\n"
        info += f"*Terminal:* {user.terminal}\n"
        info += f"*Host:* {user.host}\n"
        info += f"*Started:* {datetime.fromtimestamp(user.started).strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    return info
