"""
Report Generator
Generate daily/weekly system reports
"""
import psutil
from datetime import datetime, timedelta
from pathlib import Path
import json


class ReportGenerator:
    """Generate system reports"""
    
    def __init__(self):
        self.report_dir = Path('logs/reports')
        self.report_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_daily_report(self):
        """Generate daily system report"""
        report = {
            'type': 'daily',
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'system': self._get_system_summary(),
            'disk': self._get_disk_summary(),
            'network': self._get_network_summary(),
            'processes': self._get_process_summary(),
            'alerts': self._get_alert_summary()
        }
        
        # Save report
        filename = f"daily_{datetime.now().strftime('%Y%m%d')}.json"
        filepath = self.report_dir / filename
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def generate_weekly_report(self):
        """Generate weekly system report"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        report = {
            'type': 'weekly',
            'timestamp': end_date.isoformat(),
            'period': {
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d')
            },
            'summary': self._get_weekly_summary(),
            'system': self._get_system_summary(),
            'disk': self._get_disk_summary(),
            'alerts': self._get_alert_summary()
        }
        
        # Save report
        filename = f"weekly_{end_date.strftime('%Y%m%d')}.json"
        filepath = self.report_dir / filename
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def _get_system_summary(self):
        """Get system metrics summary"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            
            return {
                'cpu_percent': round(cpu_percent, 1),
                'cpu_count': psutil.cpu_count(),
                'memory_total_gb': round(memory.total / (1024**3), 2),
                'memory_used_gb': round(memory.used / (1024**3), 2),
                'memory_percent': memory.percent,
                'swap_total_gb': round(swap.total / (1024**3), 2),
                'swap_used_gb': round(swap.used / (1024**3), 2),
                'swap_percent': swap.percent,
                'uptime_days': uptime.days,
                'uptime_hours': uptime.seconds // 3600,
                'boot_time': boot_time.isoformat()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _get_disk_summary(self):
        """Get disk usage summary"""
        try:
            disks = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disks.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total_gb': round(usage.total / (1024**3), 2),
                        'used_gb': round(usage.used / (1024**3), 2),
                        'free_gb': round(usage.free / (1024**3), 2),
                        'percent': usage.percent
                    })
                except:
                    continue
            return disks
        except Exception as e:
            return {'error': str(e)}
    
    def _get_network_summary(self):
        """Get network stats summary"""
        try:
            net_io = psutil.net_io_counters()
            return {
                'bytes_sent_mb': round(net_io.bytes_sent / (1024**2), 2),
                'bytes_recv_mb': round(net_io.bytes_recv / (1024**2), 2),
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'errors_in': net_io.errin,
                'errors_out': net_io.errout,
                'drops_in': net_io.dropin,
                'drops_out': net_io.dropout
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _get_process_summary(self):
        """Get process summary"""
        try:
            process_count = len(psutil.pids())
            
            # Get top processes by CPU
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except:
                    continue
            
            # Sort by CPU usage
            top_cpu = sorted(processes, key=lambda x: x.get('cpu_percent', 0), reverse=True)[:5]
            
            return {
                'total_processes': process_count,
                'top_cpu_processes': [
                    {
                        'name': p['name'],
                        'cpu_percent': round(p.get('cpu_percent', 0), 1),
                        'memory_percent': round(p.get('memory_percent', 0), 1)
                    }
                    for p in top_cpu
                ]
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _get_alert_summary(self):
        """Get alert statistics"""
        try:
            from src.modules.alerts import alert_manager
            
            active = alert_manager.get_active_alerts()
            history = alert_manager.get_history(100)
            
            # Count by metric
            alert_counts = {}
            for alert in history:
                metric = alert['metric']
                alert_counts[metric] = alert_counts.get(metric, 0) + 1
            
            return {
                'active_count': len(active),
                'total_alerts_today': len([a for a in history if a['timestamp'][:10] == datetime.now().strftime('%Y-%m-%d')]),
                'alert_counts_by_metric': alert_counts
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _get_weekly_summary(self):
        """Get weekly trends and statistics"""
        # This could be enhanced to read from stored daily reports
        return {
            'note': 'Weekly trends from current snapshot',
            'days_covered': 7
        }
    
    def format_daily_report(self, report):
        """Format daily report for Telegram"""
        system = report.get('system', {})
        disk = report.get('disk', [])
        network = report.get('network', {})
        processes = report.get('processes', {})
        alerts = report.get('alerts', {})
        
        text = f"""
📊 *DAILY SYSTEM REPORT*
📅 Date: {report.get('date', 'N/A')}

*━━━━━━ SYSTEM ━━━━━━*
🔥 CPU: {system.get('cpu_percent', 0)}% ({system.get('cpu_count', 0)} cores)
🧠 Memory: {system.get('memory_percent', 0)}% ({system.get('memory_used_gb', 0)}/{system.get('memory_total_gb', 0)} GB)
💿 Swap: {system.get('swap_percent', 0)}% ({system.get('swap_used_gb', 0)}/{system.get('swap_total_gb', 0)} GB)
⏰ Uptime: {system.get('uptime_days', 0)}d {system.get('uptime_hours', 0)}h

*━━━━━━ DISK ━━━━━━*
"""
        
        # Disk info
        for d in disk[:3]:  # Top 3 disks
            text += f"💾 {d['mountpoint']}: {d['percent']}% ({d['used_gb']}/{d['total_gb']} GB)\n"
        
        text += f"""
*━━━━━━ NETWORK ━━━━━━*
📤 Sent: {network.get('bytes_sent_mb', 0)} MB
📥 Recv: {network.get('bytes_recv_mb', 0)} MB
⚠️ Errors: {network.get('errors_in', 0) + network.get('errors_out', 0)}

*━━━━━━ PROCESSES ━━━━━━*
📊 Total: {processes.get('total_processes', 0)}
Top CPU Consumers:
"""
        
        # Top processes
        for p in processes.get('top_cpu_processes', [])[:3]:
            text += f"  • {p['name']}: {p['cpu_percent']}%\n"
        
        text += f"""
*━━━━━━ ALERTS ━━━━━━*
⚠️ Active: {alerts.get('active_count', 0)}
📋 Today: {alerts.get('total_alerts_today', 0)}

_Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_
"""
        
        return text
    
    def format_weekly_report(self, report):
        """Format weekly report for Telegram"""
        period = report.get('period', {})
        system = report.get('system', {})
        disk = report.get('disk', [])
        alerts = report.get('alerts', {})
        
        text = f"""
📊 *WEEKLY SYSTEM REPORT*
📅 Period: {period.get('start', 'N/A')} to {period.get('end', 'N/A')}

*━━━━━━ CURRENT STATUS ━━━━━━*
🔥 CPU: {system.get('cpu_percent', 0)}%
🧠 Memory: {system.get('memory_percent', 0)}% ({system.get('memory_used_gb', 0)} GB used)
⏰ Uptime: {system.get('uptime_days', 0)} days

*━━━━━━ DISK STATUS ━━━━━━*
"""
        
        for d in disk[:3]:
            status = "🔴" if d['percent'] > 90 else "🟡" if d['percent'] > 80 else "🟢"
            text += f"{status} {d['mountpoint']}: {d['percent']}% ({d['used_gb']}/{d['total_gb']} GB)\n"
        
        text += f"""
*━━━━━━ ALERT SUMMARY ━━━━━━*
⚠️ Currently Active: {alerts.get('active_count', 0)}
"""
        
        # Alert breakdown
        alert_counts = alerts.get('alert_counts_by_metric', {})
        if alert_counts:
            text += "\nAlert Counts by Metric:\n"
            for metric, count in alert_counts.items():
                text += f"  • {metric.upper()}: {count}\n"
        
        text += f"""
*━━━━━━ RECOMMENDATIONS ━━━━━━*
"""
        
        # Generate recommendations
        recommendations = []
        if system.get('memory_percent', 0) > 90:
            recommendations.append("• Consider freeing up memory")
        if any(d['percent'] > 90 for d in disk):
            recommendations.append("• Disk space critical - clean up files")
        if alerts.get('active_count', 0) > 0:
            recommendations.append("• Review and resolve active alerts")
        if system.get('uptime_days', 0) > 30:
            recommendations.append("• Consider system reboot for updates")
        
        if recommendations:
            text += "\n".join(recommendations)
        else:
            text += "✅ System running smoothly!"
        
        text += f"\n\n_Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_"
        
        return text
