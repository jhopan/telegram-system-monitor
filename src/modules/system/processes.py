"""
Processes Information Module
"""
import psutil


def get_processes_info() -> str:
    """Informasi proses yang berjalan"""
    info = f"📊 *TOP PROSES (CPU)*\n\n"
    
    # Get all processes
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Sort by CPU usage
    processes = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:10]
    
    for proc in processes:
        info += f"*{proc['name']}* (PID: {proc['pid']})\n"
        info += f"  CPU: {proc['cpu_percent'] or 0:.1f}% | MEM: {proc['memory_percent'] or 0:.1f}%\n"
    
    return info
