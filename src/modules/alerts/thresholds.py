"""
Alert Thresholds Management
Store and manage alert thresholds
"""
import json
import os
from pathlib import Path


class AlertThresholds:
    """Manage alert thresholds"""
    
    def __init__(self, config_file='config/alert_thresholds.json'):
        self.config_file = Path(config_file)
        self.thresholds = self._load_thresholds()
    
    def _load_thresholds(self):
        """Load thresholds from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default thresholds
        return {
            'cpu': {
                'enabled': True,
                'threshold': 90,
                'duration': 5,  # minutes
                'last_alert': None
            },
            'memory': {
                'enabled': True,
                'threshold': 95,
                'duration': 5,
                'last_alert': None
            },
            'disk': {
                'enabled': True,
                'threshold': 90,
                'duration': 0,
                'last_alert': None
            },
            'swap': {
                'enabled': False,
                'threshold': 80,
                'duration': 5,
                'last_alert': None
            }
        }
    
    def save_thresholds(self):
        """Save thresholds to file"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.thresholds, f, indent=2)
    
    def get_threshold(self, metric):
        """Get threshold for specific metric"""
        return self.thresholds.get(metric, {})
    
    def set_threshold(self, metric, threshold, enabled=True, duration=5):
        """Set threshold for metric"""
        if metric not in self.thresholds:
            self.thresholds[metric] = {}
        
        self.thresholds[metric].update({
            'enabled': enabled,
            'threshold': threshold,
            'duration': duration
        })
        self.save_thresholds()
    
    def enable_alert(self, metric):
        """Enable alert for metric"""
        if metric in self.thresholds:
            self.thresholds[metric]['enabled'] = True
            self.save_thresholds()
    
    def disable_alert(self, metric):
        """Disable alert for metric"""
        if metric in self.thresholds:
            self.thresholds[metric]['enabled'] = False
            self.save_thresholds()
    
    def get_all_thresholds(self):
        """Get all thresholds"""
        return self.thresholds
    
    def format_thresholds_text(self):
        """Format thresholds as text"""
        text = "*🔔 ALERT THRESHOLDS*\n\n"
        
        for metric, config in self.thresholds.items():
            status = "✅ Enabled" if config.get('enabled') else "❌ Disabled"
            threshold = config.get('threshold', 0)
            duration = config.get('duration', 0)
            
            text += f"*{metric.upper()}*\n"
            text += f"  Status: {status}\n"
            text += f"  Threshold: {threshold}%\n"
            if duration > 0:
                text += f"  Duration: {duration} min\n"
            text += "\n"
        
        return text
