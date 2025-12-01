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

Ketik `/menu` untuk akses semua fitur dengan inline keyboard!

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
│   └── settings.py          # Bot config & auth
├── src/
│   ├── handlers/            # Command handlers (7 files)
│   ├── modules/             # Core modules (18 files)
│   │   ├── system/          # System monitoring (6 files)
│   │   ├── disk/            # Disk monitoring (3 files)
│   │   ├── network/         # Network monitoring (5 files)
│   │   ├── service/         # Service management (1 file)
│   │   └── device/          # Device info (3 files)
│   └── utils/               # Utilities (3 files)
└── logs/                    # Log directory
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

### Coming Soon / Ideas

- 📊 **Grafik real-time** (CPU, memory usage charts)
- 📧 **Alert notifications** (disk full, high CPU, service down)
- 🔄 **Scheduled reports** (daily/weekly system reports)
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

---

**Happy Monitoring! 🚀**

For issues, questions, atau feature requests, silakan buat issue di GitHub.
