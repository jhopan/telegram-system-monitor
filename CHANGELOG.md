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

### Enhanced

- **Inline Keyboard Navigation**: Semua fitur accessible via menu buttons
- **Multi-level Menu System**: Main → Categories → Submenus → Actions
- **Back Navigation**: Back button di semua submenu
- **Tools Menu**: Updated dengan active Alerts button (no longer "Soon")

### Technical

- Added `matplotlib==3.8.2` untuk chart generation
- Added `pillow==10.1.0` untuk image processing
- Added `APScheduler==3.10.4` untuk background tasks
- New modules: `src/modules/charts/`, `src/modules/alerts/`, `src/modules/reports/`, `src/modules/scheduler.py`
- New handlers: `alert_handlers.py`, `chart_handlers.py`, `report_handlers.py`
- Enhanced `callback_handler.py` dengan alert & report routing
- Enhanced `scheduler.py` dengan CronTrigger untuk scheduled reports

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

### Phase 1 ✅ (Current)

- ✅ Alert System dengan threshold monitoring
- ✅ Charts & Visualization
- ✅ Scheduled Reports (Daily & Weekly)
- ⏳ Process Manager Advanced (Planned)

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
