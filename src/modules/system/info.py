"""
System Information Module
"""
import platform


def get_system_info() -> str:
    """Informasi sistem lengkap"""
    uname = platform.uname()
    
    info = f"🖥️ *INFORMASI SISTEM*\n\n"
    info += f"*Sistem:* {uname.system}\n"
    info += f"*Hostname:* {uname.node}\n"
    info += f"*Release:* {uname.release}\n"
    info += f"*Version:* {uname.version}\n"
    info += f"*Machine:* {uname.machine}\n"
    info += f"*Processor:* {uname.processor or platform.processor()}\n"
    
    return info
