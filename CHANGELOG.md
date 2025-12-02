# Changelog

All notable changes to this project will be documented in this file.

## [2.1.0] - 2024-01-XX

### Added - Phase 1 Features

#### Alert System 🔔

- **Threshold Monitoring**: Configurable thresholds untuk CPU (90%), Memory (95%), Disk (90%), Swap (80%)
- **Alert Manager**: History tracking, active alerts monitoring, JSON storage
- **Alert Checker**: Background monitoring dengan sustained violation detection
- **Alert Handlers**: Full inline keyboard interface
  - Configure thresholds via buttons (70%, 80%, 90%, 95%)
  - Enable/disable per metric
  - Duration settings (1min, 5min, 10min, 30min)
  - View active alerts & history
  - Check alerts on demand
  - Clear history
- **Background Scheduler**: Automatic alert checking every 5 minutes
- **Auto Notifications**: Send alerts to admin when thresholds breached
- **Smart Notification**: Prevent spam dengan tracking notified alerts

#### Charts & Visualization 📊

- **CPU Chart**: Line chart dengan historical data (60 minutes default)
- **Memory Chart**: Pie chart + bar chart untuk RAM/SWAP usage
- **Disk Chart**: Horizontal bar chart untuk partitions dengan color-coding
- **Network Chart**: Real-time traffic monitoring (60 seconds)
- **Chart Menu**: Inline keyboard menu untuk easy access

#### Scheduled Reports 📝

- **Report Generator**: Daily & weekly system reports
- **Daily Report**: System, disk, network, processes, alerts summary
- **Weekly Report**: Period overview, trends, recommendations
- **Schedule Settings**: Configure report times via inline keyboard
  - Daily: Choose time (06:00, 09:00, 12:00, 18:00)
  - Weekly: Choose day & time
  - Enable/disable per report type
- **Report History**: View past 10 reports
- **Auto Delivery**: Scheduled reports sent to admin automatically
- **Manual Generation**: Generate on-demand via menu

#### Process Manager Advanced 🔧

- **Process Listing**: Top CPU, Top Memory, All Processes
- **Search**: Quick search by process name (Python, Nginx, MySQL, Docker, etc)
- **Filter**: By status (running, sleeping, zombie, idle) or by user
- **Process Details**: Full info (CPU, memory, threads, priority, command line)
- **Process Control**: Via inline keyboard buttons
  - Kill (SIGTERM) & Force Kill (SIGKILL)
  - Suspend & Resume
  - Change Priority (nice value: -20 to 19)
- **User Filter**: Filter processes by username
- **Status Filter**: Filter by process status
- **Real-time Actions**: All operations via button clicks
- **Safety**: Confirmation for destructive actions

#### Docker Management 🐳

- **Container Listing**: All, Running, Stopped containers
- **Container Details**: Full info (ID, name, image, status, IP, ports, env, command)
- **Container Stats**: Real-time CPU, Memory, Network I/O, Block I/O, PIDs
- **Container Logs**: View last 30 lines with refresh button
- **Container Control**: Via inline keyboard buttons
  - Start/Stop/Restart containers
  - Remove containers
  - Bulk actions: Start All, Stop All, Remove Stopped
- **Status Icons**: 🟢 Running, 🔴 Stopped, 🟡 Created, 🟠 Paused, 🔄 Restarting
- **Docker Detection**: Auto-detect Docker availability
- **Full Inline Keyboard**: Zero typing required - all via buttons!

#### Package Management 📦

- **Package Listing**: View installed packages (with pagination)
- **Upgradeable Packages**: Check for available updates
- **Package Categories**: Browse by category
  - Web Servers: nginx, apache2, lighttpd
  - Databases: mysql-server, postgresql, mongodb, redis-server
  - Dev Tools: git, curl, wget, vim, build-essential
  - Monitoring: htop, iotop, nethogs, vnstat
  - System & Security: ufw, fail2ban, unattended-upgrades
- **Package Operations**: Via inline keyboard buttons
  - Install package (with confirmation)
  - Remove package (with confirmation)
  - Update package list (apt update)
  - Upgrade all packages (apt upgrade)
  - Autoremove unused packages
- **Package Info**: Detailed information (version, size, maintainer, description)
- **Status Indicators**: ✅ Installed, 📦 Not installed
- **APT Detection**: Auto-detect APT availability
- **Full Inline Keyboard**: Zero typing required - all via buttons!

#### Firewall Management 🛡️

- **Firewall Status**: View UFW status (enabled/disabled, default policies)
- **Enable/Disable**: Toggle firewall protection dengan confirmation
- **Rules Management**: View all active rules dengan details
- **Add Rules**: Via preset service buttons
  - Common: SSH (22), HTTP (80), HTTPS (443)
  - Databases: MySQL (3306), PostgreSQL (5432), MongoDB (27017), Redis (6379)
  - Other: FTP (21), SMTP (25), DNS (53), Docker (2375)
- **Delete Rules**: Remove rules by number dengan confirmation
- **Default Policies**: Configure incoming/outgoing policies
  - Options: Allow, Deny, Reject
  - Separate controls untuk incoming dan outgoing
- **Reset Firewall**: Reset to defaults dengan confirmation
- **Status Icons**: 🟢 Active, 🔴 Inactive, 🔒 Deny, 🔓 Allow
- **UFW Detection**: Auto-detect UFW availability
- **Full Inline Keyboard**: Zero typing required - all via buttons!

#### Custom Scripts Executor 📜

- **Script Categories**: 5 preset categories
  - 🖥️ System Info: System details, users, logins, top processes
  - 🧹 Cleanup: APT clean, remove old kernels, clear logs, clear /tmp
  - 💾 Backup: Backup /etc, list backups, backup crontab
  - 🌐 Network: Network overview, open ports, ping tests, DNS check
  - ⚡ Performance: Load average, memory hogs, I/O stats, bandwidth
- **Script Execution**: Via inline keyboard dengan confirmation
- **Output Display**: Real-time output capture (max 3000 chars)
- **Script History**: Track last 50 script executions
  - Timestamp, status, category, output preview
  - Clear history option
- **Safe Execution**: 30-second timeout untuk prevent hanging
- **Script Preview**: View script content sebelum execute
- **Status Tracking**: Success/Failed indicator dengan detailed output
- **Full Inline Keyboard**: Zero typing required - all via buttons!

### Enhanced

- **Inline Keyboard Navigation**: Semua fitur accessible via menu buttons
- **Multi-level Menu System**: Main → Categories → Submenus → Actions
- **Back Navigation**: Back button di semua submenu
- **Tools Menu**: Updated dengan 8 active tools (Charts, Alerts, Reports, Processes, Docker, Packages, Firewall, Scripts)

### Technical

- Added `matplotlib==3.8.2` untuk chart generation
- Added `pillow==10.1.0` untuk image processing
- Added `APScheduler==3.10.4` untuk background tasks
- New modules: `src/modules/charts/`, `src/modules/alerts/`, `src/modules/reports/`, `src/modules/process/`, `src/modules/docker/`, `src/modules/packages/`, `src/modules/firewall/`, `src/modules/scripts/`, `src/modules/scheduler.py`
- New handlers: `alert_handlers.py`, `chart_handlers.py`, `report_handlers.py`, `process_handlers.py`, `docker_handlers.py`, `package_handlers.py`, `firewall_handlers.py`, `scripts_handlers.py`
- Enhanced `callback_handler.py` dengan alert, report, process, docker, package, firewall & scripts routing
- Enhanced `scheduler.py` dengan CronTrigger untuk scheduled reports
- Total 38 modules, 15 handlers, 80+ files

## [2.0.0] - 2024-01-XX

### Added

- **Complete Inline Keyboard System**: No typing needed, just click!
- **Multi-level Menu Navigation**: Intuitive category-based navigation
- **Separate Setup Scripts**: 3 script terpisah untuk flexible installation
  - `scripts/install.sh` - Installation & configuration
  - `scripts/setup-systemd.sh` - Systemd service setup
  - `scripts/setup-aliases.sh` - Command aliases setup

### Enhanced

- **Modular Architecture**: 50+ files dengan proper separation of concerns
  - `app/` - Application entry point
  - `src/handlers/` - Command handlers
  - `src/modules/` - Core modules (system, disk, network, service, device)
  - `src/utils/` - Utilities (decorators, helpers, formatters)
  - `config/` - Configuration & settings
- **Improved Project Structure**: Better organization untuk maintainability
- **Enhanced Documentation**: Comprehensive README dengan troubleshooting

### Technical

- Upgraded to `python-telegram-bot==20.7`
- Added `CallbackQueryHandler` untuk inline keyboards
- Enhanced decorators untuk admin authentication
- Improved error handling & logging

## [1.0.0] - Initial Release

### Features

- Basic system monitoring (CPU, Memory, Uptime, Processes, Users)
- Disk monitoring (Usage, Partitions, I/O Stats)
- Network monitoring (Interfaces, Stats, Public IP, Connections, Routing, DNS, Ping)
- Service management (List, Status, Start/Stop/Restart, Logs)
- Device information (Hardware info, Sensors, Battery)
- Admin authentication (User ID & Username)
- Command-based interface

### Technical

- Python 3.8+ support
- Dependencies: python-telegram-bot, psutil, python-dotenv, netifaces
- Systemd service support
- Logging system

---

## Development Roadmap

### Phase 1 ✅ (Completed!)

- ✅ Alert System dengan threshold monitoring
- ✅ Charts & Visualization
- ✅ Scheduled Reports (Daily & Weekly)
- ✅ Process Manager Advanced

### Phase 2 (Planned)

- Docker monitoring & management
- Package management (apt)
- Firewall control (ufw)
- Custom bash script execution

### Phase 3 (Future)

- Multi-server support
- Web dashboard
- Mobile app companion
- Advanced analytics

---

**Legend:**

- ✅ Completed
- 🔄 In Progress
- ⏳ Planned
- 💡 Idea/Consideration
