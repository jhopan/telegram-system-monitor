"""
Battery Information Module
"""
import psutil


def get_battery_info() -> str:
    """Informasi battery (untuk laptop)"""
    info = f"🔋 *INFORMASI BATTERY*\n\n"
    
    try:
        battery = psutil.sensors_battery()
        
        if battery is None:
            info += "Tidak ada battery terdeteksi (mungkin desktop PC)\n"
        else:
            info += f"*Percentage:* {battery.percent}%\n"
            info += f"*Power Plugged:* {'Yes ⚡' if battery.power_plugged else 'No 🔌'}\n"
            
            if battery.secsleft != psutil.POWER_TIME_UNLIMITED:
                hours, remainder = divmod(battery.secsleft, 3600)
                minutes, seconds = divmod(remainder, 60)
                info += f"*Time Left:* {int(hours)}h {int(minutes)}m {int(seconds)}s\n"
            else:
                info += f"*Time Left:* Unlimited (plugged in)\n"
            
            # Battery status visualization
            percent = battery.percent
            bar_length = 20
            filled = int(bar_length * percent / 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            info += f"\n`[{bar}]` {percent}%\n"
            
    except Exception as e:
        info += f"Error: {str(e)}\n"
    
    return info
