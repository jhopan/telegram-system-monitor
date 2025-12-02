# Alert System Documentation

## Overview

Alert System adalah fitur monitoring otomatis yang secara periodik memeriksa metrics sistem (CPU, Memory, Disk, Swap) dan mengirimkan notifikasi ke admin ketika threshold terlampaui.

## Features

### 1. Threshold Management

- **Configurable Thresholds**: Set threshold untuk setiap metric
- **Default Values**:
  - CPU: 90%
  - Memory: 95%
  - Disk: 90%
  - Swap: 80%
- **Enable/Disable**: Toggle monitoring per metric
- **Duration Settings**: Set minimum duration sebelum alert triggered (untuk CPU/Memory/Swap)

### 2. Alert Monitoring

- **Active Alerts**: Track alerts yang sedang active
- **Alert History**: Simpan 100 alert terakhir
- **Auto-Resolve**: Alert automatically resolved ketika metric kembali normal
- **Sustained Violation Detection**: Alert hanya triggered setelah threshold breach berlangsung sesuai duration

### 3. Notifications

- **Auto Notifications**: Kirim alert ke admin via Telegram
- **Smart Notification**: Prevent spam dengan tracking notified alerts
- **Manual Check**: Check alerts on-demand via inline keyboard

### 4. Inline Keyboard Interface

- **No Typing Needed**: Semua konfigurasi via buttons
- **Settings Menu**: Configure thresholds per metric
- **Quick Actions**: View active alerts, history, check now
- **Clear History**: Clean up old alerts

## Architecture

```
src/modules/alerts/
├── __init__.py          # Module initialization
├── thresholds.py        # AlertThresholds class
├── manager.py           # AlertManager class
└── checker.py           # AlertChecker class

src/handlers/
└── alert_handlers.py    # Telegram UI handlers

src/modules/
└── scheduler.py         # BackgroundScheduler
```

### Components

#### 1. AlertThresholds (`thresholds.py`)

Manages threshold configuration:

```python
class AlertThresholds:
    def __init__(self, config_file='config/alert_thresholds.json')
    def get_threshold(self, metric: str) -> dict
    def set_threshold(self, metric: str, threshold: int, enabled: bool = True, duration: int = 5)
    def enable_alert(self, metric: str)
    def disable_alert(self, metric: str)
    def format_thresholds_text(self) -> str
```

**Storage**: `config/alert_thresholds.json`

```json
{
  "cpu": {
    "threshold": 90,
    "enabled": true,
    "duration": 5
  },
  "memory": {
    "threshold": 95,
    "enabled": true,
    "duration": 5
  },
  "disk": {
    "threshold": 90,
    "enabled": true,
    "duration": 0
  },
  "swap": {
    "threshold": 80,
    "enabled": true,
    "duration": 10
  }
}
```

#### 2. AlertManager (`manager.py`)

Manages alert history and active alerts:

```python
class AlertManager:
    def __init__(self, history_file='logs/alert_history.json')
    def add_alert(self, metric, value, threshold, message) -> dict
    def resolve_alert(self, metric)
    def get_active_alerts(self) -> dict
    def get_history(self, limit=10) -> list
    def format_active_alerts(self) -> str
    def format_history(self, limit=10) -> str
    def clear_history()
```

**Storage**: `logs/alert_history.json`

```json
[
  {
    "metric": "cpu",
    "value": 95.2,
    "threshold": 90,
    "message": "CPU usage critical!",
    "timestamp": "2024-01-15T14:30:00",
    "resolved": false
  }
]
```

#### 3. AlertChecker (`checker.py`)

Performs actual metric checking:

```python
class AlertChecker:
    def __init__(self, thresholds: AlertThresholds, manager: AlertManager)
    def check_cpu(self) -> Optional[dict]
    def check_memory(self) -> Optional[dict]
    def check_disk(self) -> Optional[dict]
    def check_swap(self) -> Optional[dict]
    def check_all(self) -> list
```

**Features**:

- Sustained violation detection dengan duration tracking
- Auto-resolve alerts ketika metrics normal
- Return alert dict jika threshold breached

#### 4. BackgroundScheduler (`scheduler.py`)

Runs periodic tasks:

```python
class BackgroundScheduler:
    def __init__(self, bot_application)
    async def check_alerts_task()
    async def send_alert_notification(alert)
    def start(self, interval_minutes=5)
    def stop()
```

**Features**:

- Periodic alert checking (default: every 5 minutes)
- Auto-send notifications ke admin
- Track notified alerts untuk prevent spam

## Usage

### Access Alert System

Via inline keyboard:

1. Send `/menu` atau `/start`
2. Click "🛠️ Tools"
3. Click "🔔 Alerts"

Or directly: `/alerts`

### Alert Menu Options

```
🔔 ALERT SYSTEM

⚙️ Settings       - Configure thresholds
📊 Active Alerts  - View current alerts
📜 History        - View alert history
🔍 Check Now      - Manual alert check
```

### Configure Thresholds

1. Click "⚙️ Settings"
2. Choose metric (CPU, Memory, Disk, Swap)
3. Options available:
   - **Enable/Disable**: Toggle monitoring
   - **Threshold**: Choose 70%, 80%, 90%, or 95%
   - **Duration**: Choose 1min, 5min, 10min, or 30min (CPU/Memory/Swap only)

### View Active Alerts

Click "📊 Active Alerts" to see:

- Metric name
- Current value
- Threshold
- Alert message
- Timestamp

### View History

Click "📜 History" to see:

- Last 20 alerts
- Status (Active ⚠️ or Resolved ✅)
- Metric, value, threshold
- Timestamp & resolved time

### Manual Check

Click "🔍 Check Now" untuk immediate check semua metrics.

### Clear History

1. Go to History
2. Click "🗑️ Clear History"
3. Confirm

## Configuration

### Adjust Check Interval

Edit `app/main.py`:

```python
# Change interval from 5 to desired minutes
scheduler.start(interval_minutes=5)
```

### Modify Default Thresholds

Edit alert threshold defaults di `src/modules/alerts/thresholds.py`:

```python
self.default_thresholds = {
    'cpu': {'threshold': 90, 'enabled': True, 'duration': 5},
    'memory': {'threshold': 95, 'enabled': True, 'duration': 5},
    'disk': {'threshold': 90, 'enabled': True, 'duration': 0},
    'swap': {'threshold': 80, 'enabled': True, 'duration': 10}
}
```

### Alert History Retention

Edit `src/modules/alerts/manager.py`:

```python
# Keep only last 100 alerts (change 100 to desired number)
if len(self.history) > 100:
    self.history = self.history[-100:]
```

## Alert Notification Format

When alert triggered, admin receives:

```
⚠️ SYSTEM ALERT

Metric: CPU
Current Value: 95.2%
Threshold: 90%

Message: CPU usage critical! Consider checking running processes.

Use /alerts to manage alert settings
```

## Troubleshooting

### Alerts Not Working

1. **Check scheduler is running**:

   ```bash
   sudo journalctl -u telegram-monitor-bot -f | grep "scheduler"
   ```

   Should see: "Background scheduler started"

2. **Check alert configuration**:

   - Send `/alerts` → Settings
   - Verify metrics are enabled
   - Check thresholds are realistic

3. **Test manually**:
   - Go to Alerts menu
   - Click "🔍 Check Now"
   - See if any alerts detected

### No Notifications

1. **Verify admin User ID in .env**:

   ```env
   ADMIN_USER_IDS=your_user_id
   ```

2. **Check logs for errors**:

   ```bash
   sudo journalctl -u telegram-monitor-bot -n 50
   ```

3. **Test notification manually**:
   - Generate high CPU: `stress --cpu 4 --timeout 120`
   - Wait for alert check cycle

### Alert History Not Saving

1. **Check logs directory exists**:

   ```bash
   ls -la logs/
   ```

2. **Check permissions**:

   ```bash
   chmod 755 logs/
   ```

3. **Check file ownership**:
   ```bash
   ls -la logs/alert_history.json
   ```

### Threshold Not Saving

1. **Check config directory exists**:

   ```bash
   ls -la config/
   ```

2. **Check file permissions**:
   ```bash
   chmod 644 config/alert_thresholds.json
   ```

## Best Practices

1. **Set Realistic Thresholds**:

   - Don't set too low (false positives)
   - Don't set too high (miss real issues)
   - Use duration untuk filter temporary spikes

2. **Regular Monitoring**:

   - Check alert history periodically
   - Adjust thresholds berdasarkan patterns
   - Clear old history regularly

3. **Duration Settings**:

   - CPU/Memory: 5-10 minutes (filter temporary spikes)
   - Disk: 0 minutes (immediate alert)
   - Swap: 10 minutes (sustained issues only)

4. **Performance Impact**:

   - Default 5-minute interval is reasonable
   - Don't set too frequent (<1 minute)
   - Monitor bot resource usage

5. **Alert Fatigue**:
   - Use duration settings untuk reduce noise
   - Disable non-critical metrics jika terlalu banyak alerts
   - Fix recurring issues rather than ignore alerts

## Advanced Usage

### Custom Alert Logic

Extend `AlertChecker` class:

```python
def check_custom_metric(self):
    """Add custom metric checking"""
    config = self.thresholds.get_threshold('custom')
    if not config.get('enabled'):
        return None

    # Your custom check logic
    value = get_custom_metric()
    threshold = config.get('threshold', 80)

    if value > threshold:
        return self.manager.add_alert(
            'custom',
            value,
            threshold,
            'Custom metric exceeded!'
        )
```

### Add New Metrics

1. Add to thresholds defaults
2. Create check method in AlertChecker
3. Add to `check_all()` method
4. Add UI buttons in alert_handlers.py

### Integration with External Services

Send alerts to external services:

```python
async def send_alert_notification(self, alert):
    """Send to Telegram + external service"""
    # Telegram notification
    await self.bot.send_message(...)

    # External webhook
    import requests
    requests.post('https://your-webhook.com', json=alert)
```

## API Reference

See inline documentation in source files:

- `src/modules/alerts/thresholds.py`
- `src/modules/alerts/manager.py`
- `src/modules/alerts/checker.py`
- `src/modules/scheduler.py`
- `src/handlers/alert_handlers.py`

## Future Enhancements

Planned features:

- 📧 Email notifications
- 📱 SMS alerts (via Twilio)
- 🔗 Webhook integrations
- 📊 Alert analytics & patterns
- 🎯 Smart threshold recommendations
- 🔄 Alert escalation rules
- 👥 Multiple notification channels
- 📅 Alert schedule (quiet hours)

---

**Need Help?**

- Check logs: `sudo journalctl -u telegram-monitor-bot -f`
- GitHub Issues: https://github.com/jhopan/telegram-system-monitor/issues
- Telegram: Contact bot admin
