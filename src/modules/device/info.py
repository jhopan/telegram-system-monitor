"""
Device Information Module
"""
import platform
import subprocess


def get_device_info() -> str:
    """Informasi device/hardware"""
    info = f"🔧 *INFORMASI DEVICE*\n\n"
    
    # Basic info
    uname = platform.uname()
    info += f"*System:* {uname.system}\n"
    info += f"*Node Name:* {uname.node}\n"
    info += f"*Machine:* {uname.machine}\n"
    info += f"*Processor:* {uname.processor or platform.processor()}\n\n"
    
    # Try to get more hardware info from dmidecode (requires root)
    try:
        # Get system manufacturer and product
        result = subprocess.run(
            ['sudo', 'dmidecode', '-t', 'system'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            info += "*SYSTEM INFO (DMI):*\n"
            lines = result.stdout.split('\n')
            for line in lines:
                line = line.strip()
                if 'Manufacturer:' in line or 'Product Name:' in line or 'Version:' in line or 'Serial Number:' in line:
                    info += f"{line}\n"
            info += "\n"
    except:
        info += "*DMI Info:* Tidak tersedia (perlu sudo)\n\n"
    
    # USB devices
    try:
        result = subprocess.run(
            ['lsusb'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            usb_devices = result.stdout.strip().split('\n')
            info += f"*USB DEVICES:* ({len(usb_devices)})\n"
            for device in usb_devices[:10]:  # Limit to 10
                info += f"• {device}\n"
            if len(usb_devices) > 10:
                info += f"... dan {len(usb_devices) - 10} lainnya\n"
    except:
        info += "*USB Devices:* Tidak dapat membaca\n"
    
    return info
