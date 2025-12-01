"""
Configuration Management
Mengelola semua konfigurasi bot dan validasi admin
"""
import os
import logging
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Logging configuration
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = LOG_DIR / 'bot.log'

# Bot configuration
class BotConfig:
    """Bot configuration"""
    TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN', '')
    
    # Admin configuration
    ADMIN_USER_IDS: List[int] = []
    ADMIN_USERNAMES: List[str] = []
    
    # Security
    ENABLE_AUTH: bool = os.getenv('ENABLE_AUTH', 'true').lower() == 'true'
    
    # Features
    ENABLE_SERVICE_CONTROL: bool = os.getenv('ENABLE_SERVICE_CONTROL', 'true').lower() == 'true'
    MAX_MESSAGE_LENGTH: int = int(os.getenv('MAX_MESSAGE_LENGTH', '4000'))
    
    def __init__(self):
        """Initialize configuration"""
        self._load_admin_config()
        self._validate()
    
    def _load_admin_config(self):
        """Load admin configuration dari environment"""
        # Admin User IDs
        admin_ids_str = os.getenv('ADMIN_USER_IDS', '')
        if admin_ids_str:
            try:
                self.ADMIN_USER_IDS = [
                    int(uid.strip()) 
                    for uid in admin_ids_str.split(',') 
                    if uid.strip()
                ]
            except ValueError as e:
                logging.error(f"Error parsing ADMIN_USER_IDS: {e}")
                self.ADMIN_USER_IDS = []
        
        # Admin Usernames (tanpa @)
        admin_usernames_str = os.getenv('ADMIN_USERNAMES', '')
        if admin_usernames_str:
            self.ADMIN_USERNAMES = [
                username.strip().replace('@', '')
                for username in admin_usernames_str.split(',')
                if username.strip()
            ]
    
    def _validate(self):
        """Validate configuration"""
        if not self.TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan di environment variables!")
        
        if self.ENABLE_AUTH and not self.ADMIN_USER_IDS and not self.ADMIN_USERNAMES:
            logging.warning(
                "⚠️  ENABLE_AUTH=true tapi tidak ada admin yang dikonfigurasi! "
                "Bot bisa diakses oleh siapa saja. "
                "Set ADMIN_USER_IDS atau ADMIN_USERNAMES di .env"
            )
    
    def is_admin(self, user_id: int, username: Optional[str] = None) -> bool:
        """
        Cek apakah user adalah admin
        
        Args:
            user_id: Telegram user ID
            username: Telegram username (optional)
        
        Returns:
            True jika user adalah admin
        """
        if not self.ENABLE_AUTH:
            return True
        
        # Jika tidak ada admin dikonfigurasi, izinkan semua
        if not self.ADMIN_USER_IDS and not self.ADMIN_USERNAMES:
            return True
        
        # Cek user ID
        if user_id in self.ADMIN_USER_IDS:
            return True
        
        # Cek username
        if username and username.replace('@', '') in self.ADMIN_USERNAMES:
            return True
        
        return False
    
    def get_admin_info(self) -> str:
        """Get admin configuration info"""
        info = "🔐 *Admin Configuration*\n\n"
        info += f"*Authentication:* {'Enabled' if self.ENABLE_AUTH else 'Disabled'}\n"
        
        if self.ENABLE_AUTH:
            info += f"*Admin User IDs:* {len(self.ADMIN_USER_IDS)}\n"
            info += f"*Admin Usernames:* {len(self.ADMIN_USERNAMES)}\n"
            
            if self.ADMIN_USER_IDS:
                info += f"\n*Authorized User IDs:*\n"
                for uid in self.ADMIN_USER_IDS:
                    info += f"  • `{uid}`\n"
            
            if self.ADMIN_USERNAMES:
                info += f"\n*Authorized Usernames:*\n"
                for username in self.ADMIN_USERNAMES:
                    info += f"  • @{username}\n"
        else:
            info += "\n⚠️ *Warning:* Authentication disabled, siapa saja bisa akses bot!\n"
        
        return info


# Create global config instance
config = BotConfig()


# Logging setup
def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )


# Module paths
MODULES_DIR = BASE_DIR / 'src' / 'modules'
HANDLERS_DIR = BASE_DIR / 'src' / 'handlers'
