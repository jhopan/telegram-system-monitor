"""
Disk Information Module
"""
import psutil
from src.utils.formatters import format_bytes


def get_disk_info() -> str:
    """Informasi disk semua partisi"""
    info = f"💾 *INFORMASI DISK*\n\n"
    
    partitions = psutil.disk_partitions()
    for partition in partitions:
        info += f"*Device:* {partition.device}\n"
        info += f"*Mountpoint:* {partition.mountpoint}\n"
        info += f"*File system type:* {partition.fstype}\n"
        
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            info += f"*Total Size:* {format_bytes(partition_usage.total)}\n"
            info += f"*Used:* {format_bytes(partition_usage.used)} ({partition_usage.percent}%)\n"
            info += f"*Free:* {format_bytes(partition_usage.free)}\n"
        except PermissionError:
            info += "Tidak bisa mengakses partisi ini\n"
        info += "\n"
    
    # Disk IO statistics
    disk_io = psutil.disk_io_counters()
    if disk_io:
        info += f"*Total Read:* {format_bytes(disk_io.read_bytes)}\n"
        info += f"*Total Write:* {format_bytes(disk_io.write_bytes)}\n"
    
    return info
