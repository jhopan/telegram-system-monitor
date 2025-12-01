"""
Network Tools Module
Ping, Routing, DNS
"""
import subprocess
import os


def ping_host(host: str) -> str:
    """Ping ke host tertentu"""
    info = f"🏓 *PING ke {host}*\n\n"
    
    try:
        result = subprocess.run(
            ['ping', '-c', '4', host],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # Parse output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'packets transmitted' in line or 'rtt min/avg/max' in line or 'bytes from' in line:
                    info += f"{line}\n"
        else:
            info += f"❌ Ping gagal ke {host}\n"
            info += result.stderr
            
    except subprocess.TimeoutExpired:
        info += f"⏱️ Timeout saat ping ke {host}\n"
    except Exception as e:
        info += f"❌ Error: {str(e)}\n"
    
    return info


def get_routing_table() -> str:
    """Tampilkan routing table"""
    info = f"🗺️ *ROUTING TABLE*\n\n"
    
    try:
        result = subprocess.run(
            ['ip', 'route'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            info += f"```\n{result.stdout}```\n"
        else:
            info += "❌ Tidak dapat membaca routing table\n"
            
    except Exception as e:
        info += f"❌ Error: {str(e)}\n"
    
    return info


def get_dns_info() -> str:
    """Informasi DNS"""
    info = f"🔍 *INFORMASI DNS*\n\n"
    
    try:
        # Read resolv.conf
        if os.path.exists('/etc/resolv.conf'):
            with open('/etc/resolv.conf', 'r') as f:
                content = f.read()
                info += f"```\n{content}```\n"
        else:
            info += "File /etc/resolv.conf tidak ditemukan\n"
            
    except Exception as e:
        info += f"❌ Error: {str(e)}\n"
    
    return info
