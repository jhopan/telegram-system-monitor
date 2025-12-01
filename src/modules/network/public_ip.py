"""
Public IP Module
"""
import subprocess


def get_public_ip() -> str:
    """Dapatkan IP public"""
    info = f"🌍 *IP PUBLIC*\n\n"
    
    try:
        # Try using curl
        result = subprocess.run(
            ['curl', '-s', 'ifconfig.me'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            info += f"*IP Public:* {result.stdout.strip()}\n"
        else:
            # Try alternative
            result = subprocess.run(
                ['curl', '-s', 'icanhazip.com'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                info += f"*IP Public:* {result.stdout.strip()}\n"
            else:
                info += "*IP Public:* Tidak dapat dideteksi\n"
    except Exception as e:
        info += f"*IP Public:* Error - {str(e)}\n"
    
    return info
