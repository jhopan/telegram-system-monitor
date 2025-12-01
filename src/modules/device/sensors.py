"""
Sensors Information Module
Temperature, fans, etc
"""
import psutil


def get_sensors_info() -> str:
    """Informasi sensor (temperature, fans)"""
    info = f"🌡️ *INFORMASI SENSORS*\n\n"
    
    # Temperature sensors
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            info += "*TEMPERATURE:*\n"
            for name, entries in temps.items():
                info += f"\n*{name}:*\n"
                for entry in entries:
                    label = entry.label or name
                    info += f"  {label}: {entry.current}°C"
                    if entry.high:
                        info += f" (high: {entry.high}°C)"
                    if entry.critical:
                        info += f" (critical: {entry.critical}°C)"
                    info += "\n"
        else:
            info += "*Temperature:* Tidak tersedia\n"
    except Exception as e:
        info += f"*Temperature:* Error - {str(e)}\n"
    
    info += "\n"
    
    # Fan speeds
    try:
        fans = psutil.sensors_fans()
        if fans:
            info += "*FANS:*\n"
            for name, entries in fans.items():
                info += f"\n*{name}:*\n"
                for entry in entries:
                    label = entry.label or name
                    info += f"  {label}: {entry.current} RPM\n"
        else:
            info += "*Fans:* Tidak tersedia\n"
    except Exception as e:
        info += f"*Fans:* Error - {str(e)}\n"
    
    return info
