"""
Advanced Service Manager Module

Provides comprehensive systemd service management.
"""

import subprocess
from typing import List, Dict, Optional, Tuple
import json


class ServiceManager:
    """Manages systemd services with advanced features"""
    
    def __init__(self):
        """Initialize service manager"""
        self.systemctl_available = self._check_systemctl()
    
    def _check_systemctl(self) -> bool:
        """Check if systemctl is available"""
        try:
            result = subprocess.run(
                ['which', 'systemctl'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def _run_command(self, command: List[str], timeout: int = 10) -> Tuple[bool, str]:
        """Run a command and return success status and output"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return (result.returncode == 0, result.stdout if result.returncode == 0 else result.stderr)
        except subprocess.TimeoutExpired:
            return (False, "Command timed out")
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            return (False, str(e))
    
    def get_services_list(self, filter_type: Optional[str] = None) -> List[Dict]:
        """
        Get list of systemd services
        
        Args:
            filter_type: 'running', 'failed', 'enabled', 'disabled', 'all'
        
        Returns:
            List of service dictionaries
        """
        if not self.systemctl_available:
            return []
        
        cmd = ['systemctl', 'list-units', '--type=service', '--all', '--no-pager', '--no-legend']
        success, output = self._run_command(cmd)
        
        if not success:
            return []
        
        services = []
        for line in output.strip().split('\n'):
            if not line.strip() or 'service' not in line.lower():
                continue
            
            parts = line.split()
            if len(parts) >= 4:
                name = parts[0].replace('.service', '')
                load = parts[1]
                active = parts[2]
                sub = parts[3]
                description = ' '.join(parts[4:]) if len(parts) > 4 else ''
                
                # Apply filter
                if filter_type == 'running' and active != 'active':
                    continue
                elif filter_type == 'failed' and active != 'failed':
                    continue
                elif filter_type == 'enabled':
                    enabled_cmd = ['systemctl', 'is-enabled', f'{name}.service']
                    enabled_success, enabled_output = self._run_command(enabled_cmd, timeout=5)
                    if not (enabled_success and 'enabled' in enabled_output.lower()):
                        continue
                elif filter_type == 'disabled':
                    enabled_cmd = ['systemctl', 'is-enabled', f'{name}.service']
                    enabled_success, enabled_output = self._run_command(enabled_cmd, timeout=5)
                    if enabled_success and 'enabled' in enabled_output.lower():
                        continue
                
                services.append({
                    'name': name,
                    'load': load,
                    'active': active,
                    'sub': sub,
                    'description': description
                })
        
        return services
    
    def get_service_detail(self, service_name: str) -> Dict:
        """
        Get detailed information about a service
        
        Args:
            service_name: Service name (without .service)
        
        Returns:
            Service details dictionary
        """
        if not service_name.endswith('.service'):
            service_name += '.service'
        
        details = {
            'name': service_name.replace('.service', ''),
            'status': 'unknown',
            'active': 'unknown',
            'enabled': 'unknown',
            'pid': 'N/A',
            'uptime': 'N/A',
            'memory': 'N/A',
            'cpu': 'N/A',
            'description': 'N/A',
            'loaded': 'N/A'
        }
        
        # Get status
        cmd = ['systemctl', 'status', service_name, '--no-pager']
        success, output = self._run_command(cmd, timeout=10)
        
        if success or 'Active:' in output:
            lines = output.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('Loaded:'):
                    details['loaded'] = line.replace('Loaded:', '').strip()
                elif line.startswith('Active:'):
                    details['status'] = line.replace('Active:', '').strip()
                    if 'active (running)' in line:
                        details['active'] = 'active'
                    elif 'inactive' in line:
                        details['active'] = 'inactive'
                    elif 'failed' in line:
                        details['active'] = 'failed'
                elif 'Main PID:' in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        details['pid'] = parts[2]
                elif line.startswith('Memory:'):
                    details['memory'] = line.replace('Memory:', '').strip()
                elif line.startswith('CPU:'):
                    details['cpu'] = line.replace('CPU:', '').strip()
                elif 'Description:' in line or (not line.startswith('●') and 'service' not in line.lower() and len(line) > 20):
                    if details['description'] == 'N/A':
                        details['description'] = line
        
        # Check if enabled
        cmd = ['systemctl', 'is-enabled', service_name]
        success, output = self._run_command(cmd, timeout=5)
        if success:
            details['enabled'] = output.strip()
        
        return details
    
    def get_service_logs(self, service_name: str, lines: int = 50) -> str:
        """Get service logs from journalctl"""
        if not service_name.endswith('.service'):
            service_name += '.service'
        
        cmd = ['sudo', 'journalctl', '-u', service_name, '-n', str(lines), '--no-pager']
        success, output = self._run_command(cmd, timeout=15)
        
        if success and output:
            return output
        else:
            return f"❌ Unable to retrieve logs for {service_name}"
    
    def control_service(self, service_name: str, action: str) -> Tuple[bool, str]:
        """
        Control a service (start/stop/restart/reload/enable/disable)
        
        Args:
            service_name: Service name
            action: start, stop, restart, reload, enable, disable
        
        Returns:
            Tuple of (success, message)
        """
        if not service_name.endswith('.service'):
            service_name += '.service'
        
        valid_actions = ['start', 'stop', 'restart', 'reload', 'enable', 'disable']
        if action not in valid_actions:
            return (False, f"Invalid action. Must be one of: {', '.join(valid_actions)}")
        
        cmd = ['sudo', 'systemctl', action, service_name]
        success, output = self._run_command(cmd, timeout=15)
        
        if success:
            return (True, f"✅ Successfully {action}ed {service_name.replace('.service', '')}")
        else:
            return (False, f"❌ Failed to {action} {service_name.replace('.service', '')}: {output}")
    
    def get_service_dependencies(self, service_name: str) -> str:
        """Get service dependencies"""
        if not service_name.endswith('.service'):
            service_name += '.service'
        
        cmd = ['systemctl', 'list-dependencies', service_name, '--no-pager']
        success, output = self._run_command(cmd)
        
        if success:
            return output
        else:
            return f"❌ Unable to get dependencies for {service_name}"
    
    def search_services(self, query: str) -> List[Dict]:
        """Search services by name"""
        all_services = self.get_services_list('all')
        query_lower = query.lower()
        
        matching = []
        for svc in all_services:
            if query_lower in svc['name'].lower() or query_lower in svc['description'].lower():
                matching.append(svc)
        
        return matching
    
    def format_logs(self, logs: str, max_length: int = 3500) -> str:
        """Format logs for Telegram display"""
        if not logs:
            return "<i>No logs available</i>"
        
        # Truncate if too long
        if len(logs) > max_length:
            lines = logs.split('\n')
            truncated = '\n'.join(lines[:50])
            return (
                f"<pre>{truncated}</pre>\n\n"
                f"<i>... showing first 50 lines ...</i>"
            )
        
        return f"<pre>{logs}</pre>"
    
    def get_service_counts(self) -> Dict[str, int]:
        """Get counts of services by status"""
        all_services = self.get_services_list('all')
        
        running = sum(1 for s in all_services if s['active'] == 'active')
        failed = sum(1 for s in all_services if s['active'] == 'failed')
        inactive = sum(1 for s in all_services if s['active'] not in ['active', 'failed'])
        
        return {
            'total': len(all_services),
            'running': running,
            'failed': failed,
            'inactive': inactive
        }
    
    # Common services for quick access
    COMMON_SERVICES = {
        'web': {
            'nginx': '🌐 Nginx',
            'apache2': '🌐 Apache',
            'lighttpd': '🌐 Lighttpd'
        },
        'database': {
            'mysql': '🗄️ MySQL',
            'postgresql': '🐘 PostgreSQL',
            'mongodb': '🍃 MongoDB',
            'redis': '📦 Redis'
        },
        'system': {
            'ssh': '🔐 SSH',
            'cron': '⏰ Cron',
            'docker': '🐳 Docker',
            'systemd-resolved': '🌐 DNS Resolver'
        },
        'other': {
            'fail2ban': '🛡️ Fail2Ban',
            'ufw': '🔥 UFW Firewall',
            'networking': '🌐 Networking',
            'rsyslog': '📝 Syslog'
        }
    }
    
    def get_common_services(self):
        """Get common services dictionary"""
        return self.COMMON_SERVICES
    
    def get_status_icon(self, active_status: str) -> str:
        """Get status icon for service"""
        icons = {
            'active': '🟢',
            'inactive': '⭕',
            'failed': '❌',
            'activating': '🟡',
            'deactivating': '🟠'
        }
        return icons.get(active_status, '⚪')
