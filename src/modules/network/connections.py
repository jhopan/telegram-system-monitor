"""
Network Connections Module
"""
import psutil


def get_network_connections() -> str:
    """Koneksi jaringan aktif"""
    info = f"🔌 *KONEKSI AKTIF*\n\n"
    
    try:
        connections = psutil.net_connections(kind='inet')
        
        # Group by status
        conn_by_status = {}
        for conn in connections:
            status = conn.status
            if status not in conn_by_status:
                conn_by_status[status] = 0
            conn_by_status[status] += 1
        
        info += "*Ringkasan Koneksi:*\n"
        for status, count in sorted(conn_by_status.items()):
            info += f"{status}: {count}\n"
        
        # Show established connections
        info += f"\n*KONEKSI ESTABLISHED (Maksimal 15):*\n\n"
        established = [c for c in connections if c.status == 'ESTABLISHED'][:15]
        
        for conn in established:
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
            info += f"*Local:* {laddr}\n"
            info += f"*Remote:* {raddr}\n"
            
            try:
                if conn.pid:
                    proc = psutil.Process(conn.pid)
                    info += f"*Process:* {proc.name()} (PID: {conn.pid})\n"
            except:
                pass
            info += "\n"
        
    except PermissionError:
        info += "⚠️ Memerlukan permission root untuk melihat semua koneksi.\n"
        info += "Jalankan bot dengan sudo untuk info lengkap.\n"
    
    return info
