"""
Network Information Module
"""
import psutil
import socket


def get_network_info() -> str:
    """Informasi jaringan lengkap"""
    info = f"🌐 *INFORMASI JARINGAN*\n\n"
    
    # Hostname dan IP
    hostname = socket.gethostname()
    info += f"*Hostname:* {hostname}\n"
    
    try:
        local_ip = socket.gethostbyname(hostname)
        info += f"*Local IP:* {local_ip}\n"
    except:
        info += f"*Local IP:* Tidak dapat dideteksi\n"
    
    # Network interfaces
    info += f"\n*NETWORK INTERFACES:*\n\n"
    if_addrs = psutil.net_if_addrs()
    
    for interface_name, interface_addresses in if_addrs.items():
        info += f"*Interface:* {interface_name}\n"
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                info += f"  IP Address: {address.address}\n"
                info += f"  Netmask: {address.netmask}\n"
                info += f"  Broadcast IP: {address.broadcast}\n"
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                info += f"  MAC Address: {address.address}\n"
                info += f"  Netmask: {address.netmask}\n"
                info += f"  Broadcast MAC: {address.broadcast}\n"
        info += "\n"
    
    return info
