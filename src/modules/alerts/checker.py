"""
Alert Checker
Background task to check thresholds and trigger alerts
"""
import psutil
import time
from datetime import datetime, timedelta
from .thresholds import AlertThresholds
from .manager import AlertManager


class AlertChecker:
    """Check system metrics against thresholds"""
    
    def __init__(self, thresholds: AlertThresholds, manager: AlertManager):
        self.thresholds = thresholds
        self.manager = manager
        self.metric_history = {}  # Track sustained violations
    
    def check_cpu(self):
        """Check CPU usage"""
        config = self.thresholds.get_threshold('cpu')
        if not config.get('enabled'):
            return None
        
        cpu_percent = psutil.cpu_percent(interval=1)
        threshold = config['threshold']
        
        if cpu_percent >= threshold:
            # Check if sustained violation
            metric_key = 'cpu'
            if metric_key not in self.metric_history:
                self.metric_history[metric_key] = []
            
            self.metric_history[metric_key].append({
                'value': cpu_percent,
                'time': datetime.now()
            })
            
            # Check duration
            duration = config.get('duration', 0)
            if duration > 0:
                # Filter recent violations
                cutoff = datetime.now() - timedelta(minutes=duration)
                self.metric_history[metric_key] = [
                    h for h in self.metric_history[metric_key]
                    if h['time'] >= cutoff
                ]
                
                # Alert if sustained
                if len(self.metric_history[metric_key]) >= duration:
                    return self._create_alert('cpu', cpu_percent, threshold,
                        f"CPU usage has been above {threshold}% for {duration} minutes!")
            else:
                return self._create_alert('cpu', cpu_percent, threshold,
                    f"CPU usage is at {cpu_percent:.1f}%!")
        else:
            # Resolve if was active
            if 'cpu' in self.manager.active_alerts:
                self.manager.resolve_alert('cpu')
            self.metric_history.pop('cpu', None)
        
        return None
    
    def check_memory(self):
        """Check memory usage"""
        config = self.thresholds.get_threshold('memory')
        if not config.get('enabled'):
            return None
        
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        threshold = config['threshold']
        
        if memory_percent >= threshold:
            return self._create_alert('memory', memory_percent, threshold,
                f"Memory usage is at {memory_percent:.1f}%!")
        else:
            if 'memory' in self.manager.active_alerts:
                self.manager.resolve_alert('memory')
        
        return None
    
    def check_disk(self):
        """Check disk usage"""
        config = self.thresholds.get_threshold('disk')
        if not config.get('enabled'):
            return None
        
        threshold = config['threshold']
        alerts = []
        
        for partition in psutil.disk_partitions():
            if partition.fstype:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    if usage.percent >= threshold:
                        alert = self._create_alert(
                            f'disk_{partition.device}',
                            usage.percent,
                            threshold,
                            f"Disk {partition.device} at {partition.mountpoint} is {usage.percent:.1f}% full!"
                        )
                        if alert:
                            alerts.append(alert)
                except:
                    continue
        
        return alerts if alerts else None
    
    def check_swap(self):
        """Check swap usage"""
        config = self.thresholds.get_threshold('swap')
        if not config.get('enabled'):
            return None
        
        swap = psutil.swap_memory()
        if swap.total == 0:
            return None
        
        swap_percent = swap.percent
        threshold = config['threshold']
        
        if swap_percent >= threshold:
            return self._create_alert('swap', swap_percent, threshold,
                f"Swap usage is at {swap_percent:.1f}%!")
        else:
            if 'swap' in self.manager.active_alerts:
                self.manager.resolve_alert('swap')
        
        return None
    
    def check_all(self):
        """Check all metrics"""
        alerts = []
        
        # Check each metric
        for check_func in [self.check_cpu, self.check_memory, self.check_disk, self.check_swap]:
            result = check_func()
            if result:
                if isinstance(result, list):
                    alerts.extend(result)
                else:
                    alerts.append(result)
        
        return alerts
    
    def _create_alert(self, metric, value, threshold, message):
        """Create alert if not already active"""
        if metric not in self.manager.active_alerts:
            return self.manager.add_alert(metric, value, threshold, message)
        return None
