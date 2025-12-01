"""
Disk IO Statistics Module
"""
import psutil
from src.utils.formatters import format_bytes


def get_disk_io_stats() -> str:
    """Statistik IO disk"""
    info = f"📊 *DISK IO STATISTICS*\n\n"
    
    disk_io = psutil.disk_io_counters(perdisk=True)
    
    if not disk_io:
        return info + "Tidak ada data IO tersedia.\n"
    
    # Total IO
    total_io = psutil.disk_io_counters()
    if total_io:
        info += "*TOTAL IO*\n"
        info += f"*Read:* {format_bytes(total_io.read_bytes)}\n"
        info += f"*Write:* {format_bytes(total_io.write_bytes)}\n"
        info += f"*Read Count:* {total_io.read_count:,}\n"
        info += f"*Write Count:* {total_io.write_count:,}\n"
        info += f"*Read Time:* {total_io.read_time:,} ms\n"
        info += f"*Write Time:* {total_io.write_time:,} ms\n\n"
    
    # Per disk IO
    info += "*PER DISK IO*\n\n"
    for disk, io in disk_io.items():
        info += f"*Disk:* `{disk}`\n"
        info += f"  Read: {format_bytes(io.read_bytes)}\n"
        info += f"  Write: {format_bytes(io.write_bytes)}\n"
        info += f"  Read Count: {io.read_count:,}\n"
        info += f"  Write Count: {io.write_count:,}\n\n"
    
    return info
