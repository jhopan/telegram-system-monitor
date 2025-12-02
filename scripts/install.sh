#!/bin/bash

# Telegram Monitor Bot - Installation Script
# Install dependencies dan setup Python environment

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   TELEGRAM MONITOR BOT - INSTALLATION                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}[ERROR] Jangan jalankan script ini sebagai root!${NC}"
    echo "Jalankan sebagai user biasa, script akan minta sudo saat diperlukan."
    exit 1
fi

CURRENT_DIR=$(pwd)

# ============================================================================
# STEP 1: Install System Dependencies
# ============================================================================
echo -e "${YELLOW}═══ STEP 1: System Dependencies ═══${NC}"
echo "Required: python3, python3-pip, python3-venv, git, curl"
read -p "Install system dependencies? (y/n) [default: y]: " INSTALL_DEPS
INSTALL_DEPS=${INSTALL_DEPS:-y}

if [ "$INSTALL_DEPS" = "y" ]; then
    echo -e "${BLUE}[INFO] Updating package list...${NC}"
    sudo apt update
    
    echo -e "${BLUE}[INFO] Installing packages...${NC}"
    sudo apt install -y python3 python3-pip python3-venv git curl
    
    echo -e "${GREEN}✓ System dependencies installed${NC}\n"
else
    echo -e "${YELLOW}⊗ Skipped system dependencies${NC}\n"
fi

# ============================================================================
# STEP 2: Python Virtual Environment
# ============================================================================
echo -e "${YELLOW}═══ STEP 2: Python Environment ═══${NC}"

if [ -d "venv" ]; then
    echo -e "${YELLOW}[WARNING] Virtual environment already exists!${NC}"
    read -p "Recreate? (y/n) [default: n]: " RECREATE
    RECREATE=${RECREATE:-n}
    
    if [ "$RECREATE" = "y" ]; then
        echo -e "${BLUE}[INFO] Removing old venv...${NC}"
        rm -rf venv
    else
        echo -e "${YELLOW}⊗ Using existing venv${NC}\n"
    fi
fi

if [ ! -d "venv" ]; then
    echo -e "${BLUE}[INFO] Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

echo -e "${BLUE}[INFO] Activating virtual environment...${NC}"
source venv/bin/activate

echo -e "${BLUE}[INFO] Upgrading pip...${NC}"
pip install --upgrade pip

echo -e "${BLUE}[INFO] Installing Python packages...${NC}"
pip install -r requirements.txt

echo -e "${GREEN}✓ Python packages installed${NC}\n"

# ============================================================================
# STEP 3: Configuration
# ============================================================================
echo -e "${YELLOW}═══ STEP 3: Bot Configuration ═══${NC}"

# Check if .env exists
ENV_EXISTS=false
if [ -f .env ]; then
    ENV_EXISTS=true
    echo -e "${YELLOW}[WARNING] .env file already exists!${NC}"
    read -p "Reconfigure? (y/n) [default: n]: " RECONFIG
    RECONFIG=${RECONFIG:-n}
    
    if [ "$RECONFIG" != "y" ]; then
        echo -e "${YELLOW}⊗ Using existing .env configuration${NC}\n"
        
        # Still create directories and continue
        mkdir -p logs config
        echo -e "${GREEN}✓ Directories ready${NC}\n"
        
        # Show next steps
        echo -e "${GREEN}✓ Installation completed!${NC}\n"
        echo -e "${BLUE}[NEXT STEPS]${NC}"
        echo "1. Run bot: source venv/bin/activate && python3 app/main.py"
        echo "2. Setup systemd: ./scripts/setup-systemd.sh"
        echo "3. Setup aliases: ./scripts/setup-aliases.sh"
        echo ""
        exit 0
    fi
fi

# Create .env from template if doesn't exist
if [ ! -f .env ]; then
    echo -e "${BLUE}[INFO] Creating .env from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file${NC}"
fi

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                        ║${NC}"
echo -e "${BLUE}║              BOT CONFIGURATION WIZARD                  ║${NC}"
echo -e "${BLUE}║                                                        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}📋 Credentials yang diperlukan:${NC}"
echo ""
echo -e "  ${GREEN}1. Bot Token${NC}"
echo "     • Buka Telegram, cari ${BLUE}@BotFather${NC}"
echo "     • Ketik: ${YELLOW}/newbot${NC}"
echo "     • Ikuti instruksi untuk buat bot baru"
echo "     • Copy token yang diberikan (format: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz)"
echo ""
echo -e "  ${GREEN}2. Your User ID${NC}"
echo "     • Buka Telegram, cari ${BLUE}@userinfobot${NC}"
echo "     • Ketik: ${YELLOW}/start${NC}"
echo "     • Bot akan kirim User ID Anda (angka, contoh: 123456789)"
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Get Bot Token
while true; do
    read -p "🤖 Telegram Bot Token: " BOT_TOKEN
    
    if [ -z "$BOT_TOKEN" ]; then
        echo -e "${RED}❌ Token tidak boleh kosong!${NC}"
        echo ""
        continue
    fi
    
    # Basic token validation (format: number:alphanumeric)
    if [[ ! "$BOT_TOKEN" =~ ^[0-9]+:[A-Za-z0-9_-]+$ ]]; then
        echo -e "${RED}❌ Format token tidak valid!${NC}"
        echo -e "${YELLOW}   Format seharusnya: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz${NC}"
        echo ""
        continue
    fi
    
    echo -e "${GREEN}✓ Token format valid${NC}"
    break
done

echo ""

# Get Admin User ID
while true; do
    read -p "👤 Admin User ID: " ADMIN_ID
    
    if [ -z "$ADMIN_ID" ]; then
        echo -e "${RED}❌ User ID tidak boleh kosong!${NC}"
        echo ""
        continue
    fi
    
    # Validate numeric
    if ! [[ "$ADMIN_ID" =~ ^[0-9]+$ ]]; then
        echo -e "${RED}❌ User ID harus angka!${NC}"
        echo -e "${YELLOW}   Contoh: 123456789${NC}"
        echo ""
        continue
    fi
    
    echo -e "${GREEN}✓ User ID valid${NC}"
    break
done

echo ""

# Get Admin Username (optional)
read -p "📝 Admin Username (optional, tanpa @) [Enter to skip]: " ADMIN_USERNAME
if [ ! -z "$ADMIN_USERNAME" ]; then
    # Remove @ if user included it
    ADMIN_USERNAME=${ADMIN_USERNAME#@}
    echo -e "${GREEN}✓ Username: @$ADMIN_USERNAME${NC}"
fi

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Enable Authentication
echo -e "${BLUE}🔐 Security Settings:${NC}"
read -p "Enable authentication? (y/n) [default: y]: " ENABLE_AUTH_INPUT
ENABLE_AUTH_INPUT=${ENABLE_AUTH_INPUT:-y}

if [ "$ENABLE_AUTH_INPUT" = "y" ]; then
    ENABLE_AUTH_VALUE="true"
    echo -e "${GREEN}✓ Authentication enabled (recommended)${NC}"
else
    ENABLE_AUTH_VALUE="false"
    echo -e "${YELLOW}⚠️  Authentication disabled - anyone can use the bot!${NC}"
fi

echo ""

# Service Control
echo -e "${BLUE}⚙️  Service Control Settings:${NC}"
echo "   Service control allows bot to start/stop/restart systemd services"
echo "   Requires bot to run as root or with sudo privileges"
read -p "Enable service control? (y/n) [default: y]: " SERVICE_CONTROL_INPUT
SERVICE_CONTROL_INPUT=${SERVICE_CONTROL_INPUT:-y}

if [ "$SERVICE_CONTROL_INPUT" = "y" ]; then
    SERVICE_CONTROL_VALUE="true"
    echo -e "${GREEN}✓ Service control enabled${NC}"
else
    SERVICE_CONTROL_VALUE="false"
    echo -e "${YELLOW}⊗ Service control disabled${NC}"
fi

echo ""
echo -e "${BLUE}[INFO] Saving configuration...${NC}"

# Update .env file
sed -i "s|^TELEGRAM_BOT_TOKEN=.*|TELEGRAM_BOT_TOKEN=$BOT_TOKEN|" .env
sed -i "s|^ENABLE_AUTH=.*|ENABLE_AUTH=$ENABLE_AUTH_VALUE|" .env
sed -i "s|^ADMIN_USER_IDS=.*|ADMIN_USER_IDS=$ADMIN_ID|" .env
sed -i "s|^ENABLE_SERVICE_CONTROL=.*|ENABLE_SERVICE_CONTROL=$SERVICE_CONTROL_VALUE|" .env

if [ ! -z "$ADMIN_USERNAME" ]; then
    sed -i "s|^ADMIN_USERNAMES=.*|ADMIN_USERNAMES=$ADMIN_USERNAME|" .env
fi

# Secure .env file
chmod 600 .env

echo -e "${GREEN}✓ Configuration saved to .env${NC}"
echo -e "${GREEN}✓ File permissions set (600)${NC}"
echo ""

# Show configuration summary
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║            CONFIGURATION SUMMARY                       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  Bot Token:        ${GREEN}${BOT_TOKEN:0:15}...${NC}"
echo -e "  Admin User ID:    ${GREEN}$ADMIN_ID${NC}"
if [ ! -z "$ADMIN_USERNAME" ]; then
    echo -e "  Admin Username:   ${GREEN}@$ADMIN_USERNAME${NC}"
fi
echo -e "  Authentication:   ${GREEN}$ENABLE_AUTH_VALUE${NC}"
echo -e "  Service Control:  ${GREEN}$SERVICE_CONTROL_VALUE${NC}"
echo ""

# ============================================================================
# STEP 4: Create Directories
# ============================================================================
echo -e "${YELLOW}═══ STEP 4: Setup Directories ═══${NC}"
echo -e "${BLUE}[INFO] Creating required directories...${NC}"

mkdir -p logs
mkdir -p config

echo -e "${GREEN}✓ logs/ directory ready${NC}"
echo -e "${GREEN}✓ config/ directory ready${NC}"
echo ""

# ============================================================================
# STEP 5: Test Bot
# ============================================================================
echo -e "${YELLOW}═══ STEP 5: Test Bot Connection ═══${NC}"
echo ""
echo -e "${BLUE}Would you like to test the bot now?${NC}"
echo "  This will start the bot for 30 seconds to verify configuration."
echo ""
read -p "Test run bot sekarang? (y/n) [default: y]: " TEST_BOT
TEST_BOT=${TEST_BOT:-y}

if [ "$TEST_BOT" = "y" ]; then
    echo ""
    echo -e "${BLUE}[INFO] Starting bot test...${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}👉 Open Telegram dan send /start ke bot Anda${NC}"
    echo -e "${YELLOW}   Press Ctrl+C untuk stop test sebelum 30 detik${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    # Run bot with timeout
    timeout 30 python3 app/main.py 2>&1 || true
    
    echo ""
    echo -e "${GREEN}✓ Test completed${NC}"
    echo ""
    
    read -p "Did the bot respond? (y/n): " BOT_WORKING
    if [ "$BOT_WORKING" = "y" ]; then
        echo -e "${GREEN}✓ Bot is working correctly!${NC}"
    else
        echo -e "${YELLOW}⚠️  Bot may have issues. Check:${NC}"
        echo "   1. Bot token is correct"
        echo "   2. Bot is not blocked"
        echo "   3. Internet connection"
        echo "   4. Check logs: cat logs/bot.log"
    fi
    echo ""
else
    echo -e "${YELLOW}⊗ Skipped bot test${NC}"
    echo -e "${BLUE}   You can test later with: source venv/bin/activate && python3 app/main.py${NC}"
    echo ""
fi

# ============================================================================
# Summary
# ============================================================================
echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ✓ INSTALLATION COMPLETED SUCCESSFULLY!                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              INSTALLATION SUMMARY                      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  📁 Installation Directory: ${GREEN}$(pwd)${NC}"
echo -e "  ⚙️  Configuration File:    ${GREEN}$(pwd)/.env${NC}"
echo -e "  🐍 Virtual Environment:   ${GREEN}$(pwd)/venv${NC}"
echo -e "  📝 Log Directory:         ${GREEN}$(pwd)/logs${NC}"
echo ""

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                  NEXT STEPS                            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}▶ Option 1: Run Manually (untuk testing)${NC}"
echo -e "  ${GREEN}source venv/bin/activate${NC}"
echo -e "  ${GREEN}python3 app/main.py${NC}"
echo ""
echo -e "${YELLOW}▶ Option 2: Setup as Systemd Service (recommended)${NC}"
echo -e "  ${GREEN}./scripts/setup-systemd.sh${NC}"
echo "  This will run bot as background service"
echo ""
echo -e "${YELLOW}▶ Option 3: Setup Command Aliases (optional)${NC}"
echo -e "  ${GREEN}./scripts/setup-aliases.sh${NC}"
echo "  Create shortcuts like: tbot-start, tbot-stop, tbot-logs"
echo ""

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                QUICK START GUIDE                       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${GREEN}1.${NC} Open Telegram dan cari bot Anda"
echo -e "  ${GREEN}2.${NC} Send command: ${YELLOW}/start${NC}"
echo -e "  ${GREEN}3.${NC} Click ${YELLOW}/menu${NC} untuk interactive menu"
echo -e "  ${GREEN}4.${NC} Explore features via inline keyboard buttons!"
echo ""

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                 AVAILABLE FEATURES                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${GREEN}💻 System${NC}     - CPU, Memory, Uptime, Processes"
echo -e "  ${GREEN}💾 Disk${NC}       - Usage, Partitions, I/O Stats"
echo -e "  ${GREEN}🌐 Network${NC}    - Interfaces, Stats, Connections"
echo -e "  ${GREEN}⚙️  Services${NC}   - Start/Stop/Restart Services"
echo -e "  ${GREEN}🔧 Device${NC}     - Hardware, Sensors, Battery"
echo -e "  ${GREEN}📊 Charts${NC}     - Visual CPU/Memory/Disk/Network Charts"
echo -e "  ${GREEN}🔔 Alerts${NC}     - Threshold Monitoring & Notifications"
echo ""

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                TROUBLESHOOTING                         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${YELLOW}Bot tidak merespon?${NC}"
echo "    • Check logs: cat logs/bot.log"
echo "    • Verify token: cat .env | grep BOT_TOKEN"
echo "    • Test connection: curl https://api.telegram.org/bot<TOKEN>/getMe"
echo ""
echo -e "  ${YELLOW}Permission denied?${NC}"
echo "    • For service control: run bot as root or with sudo"
echo "    • For logs: chmod 755 logs/"
echo ""
echo -e "  ${YELLOW}Need help?${NC}"
echo "    • Documentation: cat README.md"
echo "    • Alert System: cat docs/ALERT_SYSTEM.md"
echo "    • GitHub Issues: https://github.com/jhopan/telegram-system-monitor/issues"
echo ""

echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   🚀 Installation complete! Happy Monitoring! 🚀       ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
