"""
Disk Partitions Module
"""
import psutil
from src.utils.formatters import format_bytes


def get_partitions_info() -> str:
    """Informasi detail partisi"""
    info = f"💿 *PARTISI DISK*\n\n"
    
    partitions = psutil.disk_partitions()
    
    for i, partition in enumerate(partitions, 1):
        info += f"*Partisi {i}*\n"
        info += f"*Device:* `{partition.device}`\n"
        info += f"*Mountpoint:* `{partition.mountpoint}`\n"
        info += f"*FSType:* {partition.fstype}\n"
        info += f"*Options:* {partition.opts}\n"
        
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            total = format_bytes(usage.total)
            used = format_bytes(usage.used)
            free = format_bytes(usage.free)
            percent = usage.percent
            
            info += f"*Total:* {total}\n"
            info += f"*Used:* {used} ({percent}%)\n"
            info += f"*Free:* {free}\n"
            
            # Progress bar
            bar_length = 20
            filled = int(bar_length * percent / 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            info += f"`[{bar}]` {percent}%\n"
            
        except PermissionError:
            info += "⚠️ Permission denied\n"
        except Exception as e:
            info += f"⚠️ Error: {str(e)}\n"
        
        info += "\n"
    
    return info
