"""
CPU Information Module
"""
import psutil


def get_cpu_info() -> str:
    """Informasi CPU"""
    cpu_freq = psutil.cpu_freq()
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    
    info = f"💻 *INFORMASI CPU*\n\n"
    info += f"*Physical cores:* {psutil.cpu_count(logical=False)}\n"
    info += f"*Total cores:* {psutil.cpu_count(logical=True)}\n"
    
    if cpu_freq:
        info += f"*Frekuensi Max:* {cpu_freq.max:.2f}Mhz\n"
        info += f"*Frekuensi Min:* {cpu_freq.min:.2f}Mhz\n"
        info += f"*Frekuensi Current:* {cpu_freq.current:.2f}Mhz\n"
    
    info += f"*CPU Usage Total:* {psutil.cpu_percent(interval=1)}%\n\n"
    info += "*CPU Usage Per Core:*\n"
    for i, percentage in enumerate(cpu_percent):
        info += f"Core {i}: {percentage}%\n"
    
    return info
