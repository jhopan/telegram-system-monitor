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

if [ ! -f .env ]; then
    echo -e "${BLUE}[INFO] Creating .env from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file${NC}"
else
    echo -e "${YELLOW}[WARNING] .env file already exists${NC}"
    read -p "Reconfigure? (y/n) [default: n]: " RECONFIG
    RECONFIG=${RECONFIG:-n}
    
    if [ "$RECONFIG" != "y" ]; then
        echo -e "${YELLOW}⊗ Using existing .env${NC}\n"
        echo -e "${GREEN}✓ Installation completed!${NC}\n"
        exit 0
    fi
fi

echo ""
echo -e "${BLUE}[INFO] Bot Configuration${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Dapatkan credentials dari:"
echo "  • Bot Token: @BotFather → /newbot"
echo "  • User ID: @userinfobot"
echo ""

read -p "Telegram Bot Token: " BOT_TOKEN
while [ -z "$BOT_TOKEN" ]; do
    echo -e "${RED}Token tidak boleh kosong!${NC}"
    read -p "Telegram Bot Token: " BOT_TOKEN
done

read -p "Admin User ID: " ADMIN_ID
while [ -z "$ADMIN_ID" ]; do
    echo -e "${RED}User ID tidak boleh kosong!${NC}"
    read -p "Admin User ID: " ADMIN_ID
done

read -p "Admin Username (optional, tanpa @): " ADMIN_USERNAME

# Update .env
sed -i "s/^TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=$BOT_TOKEN/" .env
sed -i "s/^ENABLE_AUTH=.*/ENABLE_AUTH=true/" .env
sed -i "s/^ADMIN_USER_IDS=.*/ADMIN_USER_IDS=$ADMIN_ID/" .env

if [ ! -z "$ADMIN_USERNAME" ]; then
    sed -i "s/^ADMIN_USERNAMES=.*/ADMIN_USERNAMES=$ADMIN_USERNAME/" .env
fi

chmod 600 .env

echo ""
echo -e "${GREEN}✓ Configuration saved${NC}\n"

# ============================================================================
# STEP 4: Create Logs Directory
# ============================================================================
echo -e "${YELLOW}═══ STEP 4: Setup Directories ═══${NC}"
mkdir -p logs
echo -e "${GREEN}✓ Logs directory ready${NC}\n"

# ============================================================================
# STEP 5: Test Bot
# ============================================================================
echo -e "${YELLOW}═══ STEP 5: Test Bot ═══${NC}"
read -p "Test run bot sekarang? (y/n) [default: y]: " TEST_BOT
TEST_BOT=${TEST_BOT:-y}

if [ "$TEST_BOT" = "y" ]; then
    echo -e "${BLUE}[INFO] Starting bot test (30 seconds)...${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Open Telegram dan send /start ke bot Anda"
    echo "Press Ctrl+C untuk stop test"
    echo ""
    
    timeout 30 python3 app/main.py 2>&1 | head -20 || true
    
    echo ""
    echo -e "${GREEN}✓ Test completed${NC}\n"
else
    echo -e "${YELLOW}⊗ Skipped bot test${NC}\n"
fi

# ============================================================================
# Summary
# ============================================================================
echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ✓ INSTALLATION COMPLETED!                              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${BLUE}[SUMMARY]${NC}"
echo "Installation Directory: $(pwd)"
echo "Configuration File: $(pwd)/.env"
echo "Virtual Environment: $(pwd)/venv"
echo ""

echo -e "${YELLOW}[NEXT STEPS]${NC}"
echo "1. Test bot: source venv/bin/activate && python3 app/main.py"
echo "2. Setup systemd: ./scripts/setup-systemd.sh"
echo "3. Setup aliases: ./scripts/setup-aliases.sh"
echo ""

echo -e "${BLUE}[MANUAL RUN]${NC}"
echo "source venv/bin/activate"
echo "python3 app/main.py"
echo ""

echo -e "${GREEN}Installation complete! 🚀${NC}"
