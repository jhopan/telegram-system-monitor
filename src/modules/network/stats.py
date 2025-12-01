"""
Network Statistics Module
"""
import psutil
from src.utils.formatters import format_bytes


def get_network_stats() -> str:
    """Statistik penggunaan jaringan"""
    net_io = psutil.net_io_counters()
    
    info = f"📈 *STATISTIK JARINGAN*\n\n"
    info += f"*Bytes Sent:* {format_bytes(net_io.bytes_sent)}\n"
    info += f"*Bytes Received:* {format_bytes(net_io.bytes_recv)}\n"
    info += f"*Packets Sent:* {net_io.packets_sent:,}\n"
    info += f"*Packets Received:* {net_io.packets_recv:,}\n"
    info += f"*Errors In:* {net_io.errin:,}\n"
    info += f"*Errors Out:* {net_io.errout:,}\n"
    info += f"*Drops In:* {net_io.dropin:,}\n"
    info += f"*Drops Out:* {net_io.dropout:,}\n"
    
    return info
