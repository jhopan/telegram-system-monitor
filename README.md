# 🤖 Telegram System Monitor Bot

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

Bot Telegram untuk monitoring sistem Linux/Debian secara real-time. Monitor CPU, memory, disk, network, dan services langsung dari Telegram.

## ✨ Fitur

- 🖥️ **System**: CPU, memory, uptime, processes, users
- 💾 **Disk**: Usage, partitions, I/O stats
- 🌐 **Network**: Interfaces, connections, public IP, ping, routing
- ⚙️ **Services**: List, start/stop/restart, logs
- 🔧 **Device**: Hardware info, sensors, battery
- 📊 **Charts**: Visual charts (CPU, Memory, Disk, Network)
- 🔔 **Alerts**: Automated threshold monitoring dengan notifications
- 📝 **Reports**: Scheduled daily/weekly system reports
- 🔧 **Process Manager**: Advanced process management (search, filter, kill, priority)
- 🐳 **Docker**: Docker container monitoring & management (list, start/stop, logs, stats)
- 📦 **Package Manager**: APT package management (install, remove, update, upgrade)
- 🛡️ **Firewall**: UFW firewall management (rules, enable/disable, policies)
- 📜 **Scripts**: Custom bash scripts executor (system info, cleanup, backup, network, performance)
- 🔐 **Security**: Admin authentication (User ID & Username)

## 🚀 Quick Install

```bash
# Clone repository
git clone https://github.com/jhopan/telegram-system-monitor.git
cd telegram-system-monitor

# 1. Install & Configure Bot
chmod +x scripts/*.sh
./scripts/install.sh

# 2. Setup Systemd Service (optional)
./scripts/setup-systemd.sh

# 3. Setup Command Aliases (optional)
./scripts/setup-aliases.sh
```

**3 Script Terpisah:**

- `install.sh` - Install dependencies & configure bot
- `setup-systemd.sh` - Setup systemd service dengan custom nama
- `setup-aliases.sh` - Setup command aliases yang bisa dikustomisasi

## ⚙️ Configuration

### Get Credentials

1. **Bot Token**: Chat [@BotFather](https://t.me/BotFather) → `/newbot`
2. **User ID**: Chat [@userinfobot](https://t.me/userinfobot)

### Setup .env

```env
TELEGRAM_BOT_TOKEN=your_token_here
ENABLE_AUTH=true
ADMIN_USER_IDS=your_user_id_here
ADMIN_USERNAMES=your_username
ENABLE_SERVICE_CONTROL=true
```

## 📱 Usage

### Quick Commands

```
/start      - Start bot
/menu       - Interactive menu (RECOMMENDED!)
/help       - List all commands
```

### Monitoring Commands

```bash
# System
/cpu /memory /uptime /processes /users

# Disk & Network
/disk /partitions /network /publicip /ping google.com

# Services
/services /service_status nginx /service_restart nginx
```

### Interactive Menu

Ketik `/menu` untuk akses semua fitur dengan inline keyboard! No typing needed - just click!

### Alert System 🔔

Monitor sistem secara otomatis dengan threshold alerts:

```bash
# Access alert system
/alerts

# Configure thresholds via inline keyboard:
- CPU: Default 90% (customizable)
- Memory: Default 95% (customizable)
- Disk: Default 90% (customizable)
- Swap: Default 80% (customizable)

# Features:
- Real-time monitoring (every 5 minutes)
- Auto notifications ke admin
- Alert history tracking
- Enable/disable per metric
- Sustained violation detection
```

### Visual Charts 📊

Generate visual charts untuk monitoring:

```bash
/charts              # Chart menu
/chart_cpu           # CPU usage over time
/chart_memory        # Memory/Swap pie chart
/chart_disk          # Disk usage by partition
/chart_network       # Network traffic monitoring
```

### Docker Management 🐳

Monitor dan manage Docker containers:

```bash
/docker              # Docker menu

# Features via inline keyboard:
- List containers (All, Running, Stopped)
- Container details (stats, logs, ports, env)
- Start/Stop/Restart containers
- Remove containers
- View container logs (last 30 lines)
- Real-time stats (CPU, Memory, Network I/O)
- Bulk actions (Start All, Stop All, Remove Stopped)
```

**Requirements:** Docker harus terinstall dan running pada sistem.

### Package Management 📦

Manage sistem packages dengan APT:

```bash
# Access via /menu → Tools → Packages
# Semua via inline keyboard - NO TYPING!

# Features:
- List installed packages
- Check upgradeable packages
- Browse by category:
  • Web Servers (nginx, apache2, lighttpd)
  • Databases (mysql, postgresql, mongodb, redis)
  • Dev Tools (git, curl, wget, vim)
  • Monitoring (htop, iotop, nethogs, vnstat)
  • System & Security (ufw, fail2ban)
- Install/Remove packages dengan 1 klik
- Update package list
- Upgrade all packages
- Autoremove unused packages
```

**Requirements:** APT (Debian/Ubuntu based systems).

### Firewall Management 🛡️

Manage UFW firewall dengan mudah:

```bash
# Access via /menu → Tools → Firewall
# Semua via inline keyboard - NO TYPING!

# Features:
- View firewall status
- Enable/Disable firewall
- View all rules dengan status
- Add rules by service:
  • SSH, HTTP, HTTPS
  • MySQL, PostgreSQL, MongoDB, Redis
  • FTP, SMTP, DNS, Docker
- Delete rules dengan 1 klik
- Set default policies (incoming/outgoing)
- Reset firewall
```

**Requirements:** UFW (install: `apt install ufw`).

### Custom Scripts 📜

Execute preset bash scripts dengan mudah:

```bash
# Access via /menu → Tools → Scripts
# Semua via inline keyboard - NO TYPING!

# Categories:
🖥️ System Info:
  - Detailed system information
  - Logged in users
  - Last login attempts
  - Top processes by CPU

🧹 Cleanup:
  - APT cache cleanup
  - Remove old kernels
  - Clear old logs (7 days)
  - Clear /tmp directory

💾 Backup:
  - Backup /etc directory
  - List existing backups
  - Backup crontab

🌐 Network:
  - Network overview
  - Open ports listing
  - Ping tests (multiple hosts)
  - DNS configuration check

⚡ Performance:
  - Load average & CPU stats
  - Top memory consumers
  - I/O statistics
  - Network bandwidth usage

# Features:
- Execute with confirmation
- View output in real-time
- Execution history
- Safe timeouts (30s)
```

## 🔧 Service Management

```bash
# Systemd commands
sudo systemctl start telegram-monitor-bot
sudo systemctl stop telegram-monitor-bot
sudo systemctl restart telegram-monitor-bot
sudo systemctl status telegram-monitor-bot
sudo journalctl -u telegram-monitor-bot -f

# Custom aliases (if configured via scripts/setup-aliases.sh)
tbot-start
tbot-stop
tbot-restart
tbot-status
tbot-logs
```

## 📁 Project Structure

```
telegram-monitor-bot/
├── .env.example              # Template config
├── .gitignore                # Git ignore
├── README.md                 # Dokumentasi
├── requirements.txt          # Python dependencies
├── scripts/                  # Setup scripts ⭐
│   ├── install.sh            # Installation & configuration
│   ├── setup-systemd.sh      # Systemd service setup
│   └── setup-aliases.sh      # Command aliases setup
├── app/
│   ├── __init__.py
│   └── main.py              # Entry point
├── config/
│   ├── __init__.py
│   ├── settings.py          # Bot config & auth
│   └── alert_thresholds.json # Alert settings (auto-created)
├── src/
│   ├── handlers/            # Command handlers (11 files)
│   ├── modules/             # Core modules (30 files)
│   │   ├── system/          # System monitoring (6 files)
│   │   ├── disk/            # Disk monitoring (3 files)
│   │   ├── network/         # Network monitoring (5 files)
│   │   ├── service/         # Service management (1 file)
│   │   ├── device/          # Device info (3 files)
│   │   ├── charts/          # Chart generation (1 file)
│   │   ├── alerts/          # Alert system (4 files)
│   │   ├── reports/         # Report generation (2 files)
│   │   ├── process/         # Process manager (2 files)
│   │   └── scheduler.py     # Background tasks
│   └── utils/               # Utilities (3 files)
└── logs/                    # Log directory + alert history + reports
```

## 🛠️ Troubleshooting

### Bot tidak merespon

```bash
# Check status
sudo systemctl status telegram-monitor-bot

# Check logs
sudo journalctl -u telegram-monitor-bot -n 50
```

### Access Denied

1. Cek User ID sudah benar di `.env`
2. Pastikan `ENABLE_AUTH=true`
3. Restart bot: `sudo systemctl restart telegram-monitor-bot`

### Service control tidak jalan

Service control membutuhkan bot jalan sebagai root. Edit systemd service:

```bash
sudo nano /etc/systemd/system/telegram-monitor-bot.service
# Set: User=root
sudo systemctl daemon-reload
sudo systemctl restart telegram-monitor-bot
```

## 📦 Requirements

- Python 3.8+
- Debian/Ubuntu Linux
- Systemd (for service management)

### Python Packages

```
python-telegram-bot==20.7
psutil==5.9.6
python-dotenv==1.0.0
netifaces==0.11.0
matplotlib==3.8.2
pillow==10.1.0
APScheduler==3.10.4
```

## 🔐 Security Tips

1. **Always enable authentication**:

   ```env
   ENABLE_AUTH=true
   ```

2. **Protect .env file**:

   ```bash
   chmod 600 .env
   ```

3. **Use User ID instead of Username** (lebih aman)

4. **Monitor bot logs** untuk aktivitas mencurigakan

5. **Jangan share bot token** dengan siapapun

## 🎯 Feature Recommendations

### ✅ Completed Features

- ✅ **Grafik real-time** (CPU, memory, disk, network usage charts)
- ✅ **Alert notifications** (threshold monitoring dengan auto-notification)
- ✅ **Scheduled reports** (daily/weekly system reports otomatis)
- ✅ **Process manager** (search, filter, kill, priority management)
- ✅ **Inline keyboard navigation** (no typing needed - just click!)
- ✅ **Multi-level menu system** (intuitive navigation)
- ✅ **Background scheduler** (periodic alert checking & reports)

### Coming Soon / Ideas

- 📦 **Package management** (apt update/upgrade via bot)
- 🔒 **Firewall control** (ufw management)
- 🐳 **Docker support** (container monitoring & management)
- 📝 **Custom commands** (run bash scripts)
- 🌍 **Multi-server support** (monitor multiple servers)

Want to contribute? Fork dan submit PR!

## 📄 License

MIT License - Feel free to use and modify

## 🙏 Credits

Built with:

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [psutil](https://github.com/giampaolo/psutil)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [matplotlib](https://matplotlib.org/)
- [APScheduler](https://github.com/agronholm/apscheduler)

---

**Happy Monitoring! 🚀**

For issues, questions, atau feature requests, silakan buat issue di GitHub.
