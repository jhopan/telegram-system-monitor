#!/bin/bash

# Telegram Monitor Bot - Aliases Setup
# Setup command aliases untuk kemudahan management

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
║   TELEGRAM MONITOR BOT - ALIASES SETUP                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# ============================================================================
# STEP 1: Detect Shell
# ============================================================================
echo -e "${YELLOW}═══ STEP 1: Shell Detection ═══${NC}"

SHELL_CONFIG=""
SHELL_NAME=""

if [ -f "$HOME/.bashrc" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
    SHELL_NAME="bash"
elif [ -f "$HOME/.zshrc" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
    SHELL_NAME="zsh"
else
    echo -e "${RED}[ERROR] Shell config file not found!${NC}"
    echo "Supported shells: bash (.bashrc), zsh (.zshrc)"
    exit 1
fi

echo -e "${GREEN}✓ Detected shell: $SHELL_NAME${NC}"
echo -e "${GREEN}✓ Config file: $SHELL_CONFIG${NC}\n"

# ============================================================================
# STEP 2: Get Service Name
# ============================================================================
echo -e "${YELLOW}═══ STEP 2: Service Configuration ═══${NC}"

# Try to detect existing service
DETECTED_SERVICE=""
if [ -f "/etc/systemd/system/telegram-monitor-bot.service" ]; then
    DETECTED_SERVICE="telegram-monitor-bot"
fi

if [ ! -z "$DETECTED_SERVICE" ]; then
    echo -e "${BLUE}[INFO] Detected service: $DETECTED_SERVICE${NC}"
    read -p "Use detected service? (y/n) [default: y]: " USE_DETECTED
    USE_DETECTED=${USE_DETECTED:-y}
    
    if [ "$USE_DETECTED" = "y" ]; then
        SERVICE_NAME="$DETECTED_SERVICE"
    fi
fi

if [ -z "$SERVICE_NAME" ]; then
    read -p "Systemd service name [default: telegram-monitor-bot]: " SERVICE_NAME
    SERVICE_NAME=${SERVICE_NAME:-telegram-monitor-bot}
fi

# Verify service exists
if [ ! -f "/etc/systemd/system/${SERVICE_NAME}.service" ]; then
    echo -e "${RED}[WARNING] Service $SERVICE_NAME not found!${NC}"
    read -p "Continue anyway? (y/n) [default: y]: " CONTINUE
    CONTINUE=${CONTINUE:-y}
    
    if [ "$CONTINUE" != "y" ]; then
        echo -e "${RED}[ABORTED] Setup cancelled.${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✓ Service name: $SERVICE_NAME${NC}\n"

# ============================================================================
# STEP 3: Configure Aliases
# ============================================================================
echo -e "${YELLOW}═══ STEP 3: Alias Configuration ═══${NC}"
echo -e "${BLUE}[INFO] Customize your command aliases${NC}"
echo "Leave empty to use default"
echo ""

read -p "Start command [default: tbot-start]: " ALIAS_START
ALIAS_START=${ALIAS_START:-tbot-start}

read -p "Stop command [default: tbot-stop]: " ALIAS_STOP
ALIAS_STOP=${ALIAS_STOP:-tbot-stop}

read -p "Restart command [default: tbot-restart]: " ALIAS_RESTART
ALIAS_RESTART=${ALIAS_RESTART:-tbot-restart}

read -p "Status command [default: tbot-status]: " ALIAS_STATUS
ALIAS_STATUS=${ALIAS_STATUS:-tbot-status}

read -p "Logs command [default: tbot-logs]: " ALIAS_LOGS
ALIAS_LOGS=${ALIAS_LOGS:-tbot-logs}

read -p "Enable command [default: tbot-enable]: " ALIAS_ENABLE
ALIAS_ENABLE=${ALIAS_ENABLE:-tbot-enable}

read -p "Disable command [default: tbot-disable]: " ALIAS_DISABLE
ALIAS_DISABLE=${ALIAS_DISABLE:-tbot-disable}

echo ""
echo -e "${GREEN}✓ Aliases configured:${NC}"
echo "  Start:   $ALIAS_START"
echo "  Stop:    $ALIAS_STOP"
echo "  Restart: $ALIAS_RESTART"
echo "  Status:  $ALIAS_STATUS"
echo "  Logs:    $ALIAS_LOGS"
echo "  Enable:  $ALIAS_ENABLE"
echo "  Disable: $ALIAS_DISABLE"
echo ""

# ============================================================================
# STEP 4: Add Aliases
# ============================================================================
echo -e "${YELLOW}═══ STEP 4: Add Aliases ═══${NC}"

# Check if aliases already exist
if grep -q "# Telegram Monitor Bot Aliases" "$SHELL_CONFIG" 2>/dev/null; then
    echo -e "${YELLOW}[WARNING] Aliases already exist in $SHELL_CONFIG${NC}"
    read -p "Replace existing aliases? (y/n) [default: y]: " REPLACE
    REPLACE=${REPLACE:-y}
    
    if [ "$REPLACE" = "y" ]; then
        echo -e "${BLUE}[INFO] Removing old aliases...${NC}"
        # Remove old aliases block
        sed -i '/# Telegram Monitor Bot Aliases/,/# End Telegram Monitor Bot Aliases/d' "$SHELL_CONFIG"
    else
        echo -e "${RED}[ABORTED] Setup cancelled.${NC}"
        exit 1
    fi
fi

echo -e "${BLUE}[INFO] Adding aliases to $SHELL_CONFIG...${NC}"

# Add aliases
cat >> "$SHELL_CONFIG" << EOF

# Telegram Monitor Bot Aliases (added $(date +"%Y-%m-%d %H:%M:%S"))
alias $ALIAS_START='sudo systemctl start $SERVICE_NAME'
alias $ALIAS_STOP='sudo systemctl stop $SERVICE_NAME'
alias $ALIAS_RESTART='sudo systemctl restart $SERVICE_NAME'
alias $ALIAS_STATUS='sudo systemctl status $SERVICE_NAME'
alias $ALIAS_LOGS='sudo journalctl -u $SERVICE_NAME -f'
alias $ALIAS_ENABLE='sudo systemctl enable $SERVICE_NAME'
alias $ALIAS_DISABLE='sudo systemctl disable $SERVICE_NAME'
# End Telegram Monitor Bot Aliases
EOF

echo -e "${GREEN}✓ Aliases added to $SHELL_CONFIG${NC}\n"

# ============================================================================
# STEP 5: Test Aliases
# ============================================================================
echo -e "${YELLOW}═══ STEP 5: Reload Shell Config ═══${NC}"

echo -e "${BLUE}[INFO] Reloading shell configuration...${NC}"
source "$SHELL_CONFIG"

echo -e "${GREEN}✓ Configuration reloaded${NC}\n"

# ============================================================================
# Summary
# ============================================================================
echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ✓ ALIASES SETUP COMPLETED!                             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${BLUE}[AVAILABLE COMMANDS]${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$ALIAS_START      - Start bot service"
echo "$ALIAS_STOP       - Stop bot service"
echo "$ALIAS_RESTART    - Restart bot service"
echo "$ALIAS_STATUS     - Check service status"
echo "$ALIAS_LOGS       - View real-time logs"
echo "$ALIAS_ENABLE     - Enable auto-start on boot"
echo "$ALIAS_DISABLE    - Disable auto-start"
echo ""

echo -e "${YELLOW}[IMPORTANT]${NC}"
echo "• Aliases aktif di terminal session baru"
echo "• Atau jalankan: source $SHELL_CONFIG"
echo ""

echo -e "${BLUE}[TEST ALIAS]${NC}"
echo "Try: $ALIAS_STATUS"
echo ""

echo -e "${GREEN}Aliases ready to use! 🚀${NC}"
