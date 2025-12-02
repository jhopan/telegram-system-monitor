"""
Alert Manager
Manage alerts and notifications
"""
import json
from datetime import datetime
from pathlib import Path


class AlertManager:
    """Manage alert history and notifications"""
    
    def __init__(self, history_file='logs/alert_history.json'):
        self.history_file = Path(history_file)
        self.history = self._load_history()
        self.active_alerts = {}
    
    def _load_history(self):
        """Load alert history"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_history(self):
        """Save alert history"""
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        # Keep only last 100 alerts
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def add_alert(self, metric, value, threshold, message):
        """Add new alert"""
        alert = {
            'metric': metric,
            'value': value,
            'threshold': threshold,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'resolved': False
        }
        
        self.history.append(alert)
        self.active_alerts[metric] = alert
        self._save_history()
        
        return alert
    
    def resolve_alert(self, metric):
        """Mark alert as resolved"""
        if metric in self.active_alerts:
            del self.active_alerts[metric]
        
        # Update history
        for alert in reversed(self.history):
            if alert['metric'] == metric and not alert['resolved']:
                alert['resolved'] = True
                alert['resolved_at'] = datetime.now().isoformat()
                break
        
        self._save_history()
    
    def get_active_alerts(self):
        """Get all active alerts"""
        return self.active_alerts
    
    def get_history(self, limit=10):
        """Get alert history"""
        return self.history[-limit:]
    
    def format_active_alerts(self):
        """Format active alerts as text"""
        if not self.active_alerts:
            return "*🔔 ACTIVE ALERTS*\n\n✅ No active alerts"
        
        text = "*🔔 ACTIVE ALERTS*\n\n"
        for metric, alert in self.active_alerts.items():
            text += f"⚠️ *{metric.upper()}*\n"
            text += f"  Value: {alert['value']}%\n"
            text += f"  Threshold: {alert['threshold']}%\n"
            text += f"  Message: {alert['message']}\n"
            text += f"  Time: {alert['timestamp'][:19]}\n\n"
        
        return text
    
    def format_history(self, limit=10):
        """Format alert history as text"""
        history = self.get_history(limit)
        
        if not history:
            return "*📜 ALERT HISTORY*\n\n📭 No alerts yet"
        
        text = "*📜 ALERT HISTORY*\n"
        text += f"_(Last {len(history)} alerts)_\n\n"
        
        for alert in reversed(history):
            status = "✅" if alert.get('resolved') else "⚠️"
            text += f"{status} *{alert['metric'].upper()}*\n"
            text += f"  Value: {alert['value']}% (threshold: {alert['threshold']}%)\n"
            text += f"  Time: {alert['timestamp'][:19]}\n"
            if alert.get('resolved'):
                text += f"  Resolved: {alert.get('resolved_at', 'N/A')[:19]}\n"
            text += "\n"
        
        return text
    
    def clear_history(self):
        """Clear alert history"""
        self.history = []
        self._save_history()
