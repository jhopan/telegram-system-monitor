# Setup Scripts

Folder ini berisi 3 script terpisah untuk setup bot:

## 📋 Script Overview

### 1. `install.sh` - Installation & Configuration

**Purpose**: Install dependencies dan setup bot

**What it does:**

- ✅ Install system dependencies (python3, pip, venv, git, curl)
- ✅ Create Python virtual environment
- ✅ Install Python packages dari requirements.txt
- ✅ Create & configure .env file
- ✅ Setup logs directory
- ✅ Optional bot test run

**Usage:**

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

**Interactive prompts:**

- Install system dependencies? (y/n)
- Bot Token (dari @BotFather)
- Admin User ID (dari @userinfobot)
- Admin Username (optional)
- Test bot? (y/n)

---

### 2. `setup-systemd.sh` - Systemd Service Setup

**Purpose**: Setup bot sebagai systemd service untuk auto-start

**What it does:**

- ✅ Create systemd service file dengan custom nama
- ✅ Configure service user (root/user)
- ✅ Enable auto-start on boot
- ✅ Optional start service immediately

**Usage:**

```bash
chmod +x scripts/setup-systemd.sh
./scripts/setup-systemd.sh
```

**Interactive prompts:**

- Service name (default: telegram-monitor-bot)
- Service user (default: root)
- Service description (optional)
- Start service now? (y/n)

**Result:**

- Service file: `/etc/systemd/system/<service-name>.service`
- Auto-start enabled
- Service commands available

---

### 3. `setup-aliases.sh` - Command Aliases Setup

**Purpose**: Create command shortcuts untuk kemudahan management

**What it does:**

- ✅ Detect shell (bash/zsh)
- ✅ Create custom aliases dengan nama bebas
- ✅ Add aliases ke shell config (.bashrc/.zshrc)
- ✅ Auto-reload shell config

**Usage:**

```bash
chmod +x scripts/setup-aliases.sh
./scripts/setup-aliases.sh
```

**Interactive prompts:**

- Service name (auto-detect atau manual input)
- Custom alias untuk start (default: tbot-start)
- Custom alias untuk stop (default: tbot-stop)
- Custom alias untuk restart (default: tbot-restart)
- Custom alias untuk status (default: tbot-status)
- Custom alias untuk logs (default: tbot-logs)
- Custom alias untuk enable (default: tbot-enable)
- Custom alias untuk disable (default: tbot-disable)

**Result:**

- Aliases added to `~/.bashrc` or `~/.zshrc`
- Commands available in new terminal sessions

---

## 🚀 Complete Setup Flow

### Recommended Order:

```bash
# Step 1: Install & Configure
./scripts/install.sh

# Step 2: Setup Systemd (optional but recommended)
./scripts/setup-systemd.sh

# Step 3: Setup Aliases (optional)
./scripts/setup-aliases.sh
```

### Quick Setup (All at once):

```bash
chmod +x scripts/*.sh
./scripts/install.sh && ./scripts/setup-systemd.sh && ./scripts/setup-aliases.sh
```

---

## 📝 Examples

### Example 1: Basic Setup

```bash
# Install only, manual run
./scripts/install.sh

# Run manually
source venv/bin/activate
python3 app/main.py
```

### Example 2: Full Auto Setup

```bash
# Install + Systemd + Aliases
./scripts/install.sh
./scripts/setup-systemd.sh
./scripts/setup-aliases.sh

# Use custom aliases
tbot-start    # Start bot
tbot-status   # Check status
tbot-logs     # View logs
```

### Example 3: Custom Service Name

```bash
./scripts/install.sh

# Setup systemd dengan nama custom
./scripts/setup-systemd.sh
# Input: mybot (sebagai service name)

# Setup aliases untuk service custom
./scripts/setup-aliases.sh
# Input: mybot (sebagai service name)
# Custom aliases: bot-start, bot-stop, etc
```

---

## 🔧 Script Features

### All Scripts Support:

- ✅ Interactive prompts dengan defaults
- ✅ Color-coded output
- ✅ Error handling
- ✅ Validation checks
- ✅ Clear status messages
- ✅ Non-root execution (sudo when needed)

### Safety Features:

- Check existing files/services
- Confirmation prompts for overwrites
- Validation of inputs
- Rollback support
- Detailed error messages

---

## 🛠️ Troubleshooting

### Script won't run

```bash
# Fix permissions
chmod +x scripts/*.sh

# Check line endings (if cloned on Windows)
dos2unix scripts/*.sh
```

### Install fails

```bash
# Check internet connection
ping -c 3 google.com

# Check Python version
python3 --version  # Need 3.8+

# Check sudo access
sudo -v
```

### Systemd service fails

```bash
# Check service status
sudo systemctl status <service-name>

# Check logs
sudo journalctl -u <service-name> -n 50

# Verify .env file exists
ls -la .env

# Test manual run
source venv/bin/activate
python3 app/main.py
```

### Aliases not working

```bash
# Reload shell config
source ~/.bashrc  # or ~/.zshrc

# Check if aliases added
grep "Telegram Monitor Bot" ~/.bashrc

# Start new terminal session
```

---

## 💡 Tips

1. **Run scripts in order** (install → systemd → aliases)
2. **Use defaults** untuk quick setup
3. **Customize names** untuk multiple bots
4. **Test after each step** untuk catch errors early
5. **Keep service name consistent** across scripts
6. **Backup .env** sebelum reconfigure

---

## 📖 Related Documentation

- Main README: `../README.md`
- Environment Config: `../.env.example`
- Requirements: `../requirements.txt`

---

**Need help?** Check main README atau create issue di GitHub.
