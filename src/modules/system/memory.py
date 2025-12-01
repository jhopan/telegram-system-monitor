"""
Memory Information Module
"""
import psutil
from src.utils.formatters import format_bytes


def get_memory_info() -> str:
    """Informasi RAM"""
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    info = f"🧠 *INFORMASI MEMORY*\n\n"
    info += f"*Total:* {format_bytes(svmem.total)}\n"
    info += f"*Available:* {format_bytes(svmem.available)}\n"
    info += f"*Used:* {format_bytes(svmem.used)} ({svmem.percent}%)\n"
    info += f"*Free:* {format_bytes(svmem.free)}\n\n"
    
    info += f"*SWAP MEMORY*\n"
    info += f"*Total:* {format_bytes(swap.total)}\n"
    info += f"*Free:* {format_bytes(swap.free)}\n"
    info += f"*Used:* {format_bytes(swap.used)} ({swap.percent}%)\n"
    
    return info
