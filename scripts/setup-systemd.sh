#!/bin/bash

# Telegram Monitor Bot - Systemd Service Setup
# Setup systemd service untuk auto-start

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
║   TELEGRAM MONITOR BOT - SYSTEMD SETUP                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}[ERROR] Jangan jalankan script ini sebagai root!${NC}"
    echo "Script akan minta sudo saat diperlukan."
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}[ERROR] File .env tidak ditemukan!${NC}"
    echo "Jalankan ./scripts/install.sh terlebih dahulu"
    exit 1
fi

INSTALL_DIR=$(pwd)

# ============================================================================
# STEP 1: Service Configuration
# ============================================================================
echo -e "${YELLOW}═══ STEP 1: Service Configuration ═══${NC}"

read -p "Service name [default: telegram-monitor-bot]: " SERVICE_NAME
SERVICE_NAME=${SERVICE_NAME:-telegram-monitor-bot}

echo ""
echo -e "${BLUE}[INFO] Service User Configuration${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "• root     : Full access (recommended untuk service control)"
echo "• $USER  : Limited access (lebih aman, tanpa service control)"
echo ""

read -p "Run service as user [default: root]: " SERVICE_USER
SERVICE_USER=${SERVICE_USER:-root}

read -p "Service description [default: Telegram System Monitor Bot]: " SERVICE_DESC
SERVICE_DESC=${SERVICE_DESC:-Telegram System Monitor Bot}

echo ""
echo -e "${GREEN}✓ Service configuration:${NC}"
echo "  Name: $SERVICE_NAME"
echo "  User: $SERVICE_USER"
echo "  Description: $SERVICE_DESC"
echo ""

# ============================================================================
# STEP 2: Create Systemd Service
# ============================================================================
echo -e "${YELLOW}═══ STEP 2: Create Systemd Service ═══${NC}"

SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

if [ -f "$SERVICE_FILE" ]; then
    echo -e "${YELLOW}[WARNING] Service $SERVICE_NAME already exists!${NC}"
    read -p "Overwrite? (y/n) [default: n]: " OVERWRITE
    OVERWRITE=${OVERWRITE:-n}
    
    if [ "$OVERWRITE" != "y" ]; then
        echo -e "${RED}[ABORTED] Setup cancelled.${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}[INFO] Stopping existing service...${NC}"
    sudo systemctl stop "$SERVICE_NAME" 2>/dev/null || true
    sudo systemctl disable "$SERVICE_NAME" 2>/dev/null || true
fi

echo -e "${BLUE}[INFO] Creating systemd service file...${NC}"

sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=$SERVICE_DESC
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$INSTALL_DIR
Environment="PATH=$INSTALL_DIR/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=$INSTALL_DIR/venv/bin/python3 $INSTALL_DIR/app/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=$SERVICE_NAME

# Security
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✓ Service file created: $SERVICE_FILE${NC}\n"

# ============================================================================
# STEP 3: Enable and Start Service
# ============================================================================
echo -e "${YELLOW}═══ STEP 3: Enable Service ═══${NC}"

echo -e "${BLUE}[INFO] Reloading systemd daemon...${NC}"
sudo systemctl daemon-reload

echo -e "${BLUE}[INFO] Enabling service...${NC}"
sudo systemctl enable "$SERVICE_NAME"

echo -e "${GREEN}✓ Service enabled (auto-start on boot)${NC}\n"

read -p "Start service now? (y/n) [default: y]: " START_NOW
START_NOW=${START_NOW:-y}

if [ "$START_NOW" = "y" ]; then
    echo -e "${BLUE}[INFO] Starting service...${NC}"
    sudo systemctl start "$SERVICE_NAME"
    
    sleep 2
    
    echo ""
    echo -e "${BLUE}[INFO] Service Status:${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    sudo systemctl status "$SERVICE_NAME" --no-pager -l
    echo ""
    
    if sudo systemctl is-active --quiet "$SERVICE_NAME"; then
        echo -e "${GREEN}✓ Service running successfully!${NC}\n"
    else
        echo -e "${RED}✗ Service failed to start!${NC}"
        echo "Check logs: sudo journalctl -u $SERVICE_NAME -n 50"
        echo ""
        exit 1
    fi
else
    echo -e "${YELLOW}⊗ Service not started${NC}\n"
fi

# ============================================================================
# Summary
# ============================================================================
echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ✓ SYSTEMD SETUP COMPLETED!                             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${BLUE}[SERVICE COMMANDS]${NC}"
echo "Start:   sudo systemctl start $SERVICE_NAME"
echo "Stop:    sudo systemctl stop $SERVICE_NAME"
echo "Restart: sudo systemctl restart $SERVICE_NAME"
echo "Status:  sudo systemctl status $SERVICE_NAME"
echo "Enable:  sudo systemctl enable $SERVICE_NAME"
echo "Disable: sudo systemctl disable $SERVICE_NAME"
echo ""

echo -e "${BLUE}[VIEW LOGS]${NC}"
echo "Real-time: sudo journalctl -u $SERVICE_NAME -f"
echo "Last 50:   sudo journalctl -u $SERVICE_NAME -n 50"
echo "Today:     sudo journalctl -u $SERVICE_NAME --since today"
echo ""

echo -e "${YELLOW}[NEXT STEPS]${NC}"
echo "1. Test bot di Telegram (send /start)"
echo "2. Setup command aliases: ./scripts/setup-aliases.sh"
echo ""

echo -e "${GREEN}Systemd service ready! 🚀${NC}"
