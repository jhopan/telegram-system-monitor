"""
Logs Manager Module

Provides system logs viewing functionality.
"""

import subprocess
from typing import List, Tuple, Optional
from pathlib import Path


class LogsManager:
    """Manages system logs viewing"""
    
    def __init__(self):
        """Initialize logs manager"""
        self.journalctl_available = self._check_journalctl()
    
    def _check_journalctl(self) -> bool:
        """Check if journalctl is available"""
        try:
            result = subprocess.run(
                ['which', 'journalctl'],
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
            return (result.returncode == 0, result.stdout)
        except subprocess.TimeoutExpired:
            return (False, "Command timed out")
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            return (False, str(e))
    
    def get_journal_logs(
        self,
        lines: int = 50,
        priority: Optional[str] = None,
        since: Optional[str] = None,
        unit: Optional[str] = None
    ) -> str:
        """
        Get systemd journal logs
        
        Args:
            lines: Number of lines to retrieve
            priority: Priority level (err, warning, info, debug)
            since: Time range (1h, 6h, 24h, 7d)
            unit: Specific systemd unit
        
        Returns:
            Log content
        """
        if not self.journalctl_available:
            return "❌ journalctl not available"
        
        cmd = ['sudo', 'journalctl', '-n', str(lines), '--no-pager']
        
        if priority:
            cmd.extend(['-p', priority])
        
        if since:
            cmd.extend(['--since', since])
        
        if unit:
            cmd.extend(['-u', unit])
        
        success, output = self._run_command(cmd, timeout=15)
        
        if success and output:
            return output
        else:
            return "No logs available or error retrieving logs."
    
    def get_auth_logs(self, lines: int = 50) -> str:
        """Get authentication logs"""
        auth_log = Path('/var/log/auth.log')
        
        if not auth_log.exists():
            return "❌ /var/log/auth.log not found"
        
        cmd = ['sudo', 'tail', '-n', str(lines), str(auth_log)]
        success, output = self._run_command(cmd)
        
        return output if success else "Error reading auth.log"
    
    def get_syslog(self, lines: int = 50) -> str:
        """Get system logs"""
        syslog = Path('/var/log/syslog')
        
        if not syslog.exists():
            return "❌ /var/log/syslog not found"
        
        cmd = ['sudo', 'tail', '-n', str(lines), str(syslog)]
        success, output = self._run_command(cmd)
        
        return output if success else "Error reading syslog"
    
    def get_kernel_logs(self, lines: int = 50) -> str:
        """Get kernel logs"""
        if self.journalctl_available:
            cmd = ['sudo', 'journalctl', '-k', '-n', str(lines), '--no-pager']
        else:
            cmd = ['sudo', 'dmesg', '-T', '|', 'tail', '-n', str(lines)]
        
        success, output = self._run_command(cmd)
        return output if success else "Error reading kernel logs"
    
    def get_application_log(self, app_name: str, lines: int = 50) -> str:
        """
        Get application-specific logs
        
        Args:
            app_name: Application name (nginx, apache2, mysql, docker, etc.)
            lines: Number of lines
        
        Returns:
            Log content
        """
        # Try systemd unit first
        if self.journalctl_available:
            cmd = ['sudo', 'journalctl', '-u', app_name, '-n', str(lines), '--no-pager']
            success, output = self._run_command(cmd)
            if success and output and 'No entries' not in output:
                return output
        
        # Fallback to common log file locations
        log_paths = {
            'nginx': ['/var/log/nginx/error.log', '/var/log/nginx/access.log'],
            'apache2': ['/var/log/apache2/error.log', '/var/log/apache2/access.log'],
            'mysql': ['/var/log/mysql/error.log'],
            'postgresql': ['/var/log/postgresql/postgresql.log'],
            'docker': ['/var/log/docker.log'],
            'redis': ['/var/log/redis/redis-server.log']
        }
        
        if app_name in log_paths:
            for log_path in log_paths[app_name]:
                log_file = Path(log_path)
                if log_file.exists():
                    cmd = ['sudo', 'tail', '-n', str(lines), str(log_file)]
                    success, output = self._run_command(cmd)
                    if success and output:
                        return f"=== {log_path} ===\n\n{output}"
        
        return f"❌ No logs found for {app_name}"
    
    def search_logs(self, query: str, lines: int = 50) -> str:
        """Search logs for a query"""
        if not self.journalctl_available:
            return "❌ Search requires journalctl"
        
        cmd = ['sudo', 'journalctl', '-n', str(lines), '--no-pager', '--grep', query]
        success, output = self._run_command(cmd, timeout=15)
        
        if success and output:
            return output
        else:
            return f"No matches found for: {query}"
    
    def format_logs(self, logs: str, max_length: int = 3500) -> str:
        """Format logs for Telegram display"""
        if not logs:
            return "<i>No logs available</i>"
        
        # Truncate if too long
        if len(logs) > max_length:
            lines = logs.split('\n')
            truncated = '\n'.join(lines[:50])  # First 50 lines
            return (
                f"<pre>{truncated}</pre>\n\n"
                f"<i>... showing first 50 lines ...</i>"
            )
        
        return f"<pre>{logs}</pre>"
    
    def get_log_summary(self) -> str:
        """Get a summary of recent log activity"""
        summary_lines = []
        
        # System errors (last hour)
        if self.journalctl_available:
            cmd = ['sudo', 'journalctl', '-p', 'err', '--since', '1h', '--no-pager']
            success, output = self._run_command(cmd)
            error_count = len(output.split('\n')) if success else 0
            summary_lines.append(f"❌ Errors (last 1h): {error_count}")
            
            # Warnings (last hour)
            cmd = ['sudo', 'journalctl', '-p', 'warning', '--since', '1h', '--no-pager']
            success, output = self._run_command(cmd)
            warning_count = len(output.split('\n')) if success else 0
            summary_lines.append(f"⚠️ Warnings (last 1h): {warning_count}")
        
        # Failed SSH attempts
        auth_log = Path('/var/log/auth.log')
        if auth_log.exists():
            cmd = ['sudo', 'grep', 'Failed password', str(auth_log), '|', 'tail', '-n', '100']
            success, output = self._run_command(cmd)
            failed_ssh = len(output.split('\n')) if success else 0
            summary_lines.append(f"🔐 Failed SSH (recent): {failed_ssh}")
        
        return '\n'.join(summary_lines) if summary_lines else "No summary available"
    
    # Preset log configurations
    LOG_TYPES = {
        'system': {
            'name': '🖥️ System Logs',
            'description': 'General system logs (journalctl)',
            'method': 'journal'
        },
        'auth': {
            'name': '🔐 Authentication Logs',
            'description': 'Login attempts and auth events',
            'method': 'auth'
        },
        'kernel': {
            'name': '⚙️ Kernel Logs',
            'description': 'Kernel messages and errors',
            'method': 'kernel'
        },
        'syslog': {
            'name': '📋 Syslog',
            'description': 'System event logs',
            'method': 'syslog'
        }
    }
    
    APPLICATIONS = {
        'nginx': '🌐 Nginx',
        'apache2': '🌐 Apache',
        'mysql': '🗄️ MySQL',
        'postgresql': '🐘 PostgreSQL',
        'docker': '🐳 Docker',
        'redis': '📦 Redis',
        'ssh': '🔐 SSH (sshd)'
    }
    
    PRIORITIES = {
        'err': '❌ Errors Only',
        'warning': '⚠️ Warnings & Errors',
        'info': 'ℹ️ Info & Above',
        'debug': '🔍 All (including Debug)'
    }
    
    TIME_RANGES = {
        '1h': '⏱️ Last Hour',
        '6h': '⏱️ Last 6 Hours',
        '24h': '📅 Last 24 Hours',
        '7d': '📅 Last 7 Days'
    }
    
    def get_log_types(self):
        """Get available log types"""
        return self.LOG_TYPES
    
    def get_applications(self):
        """Get available applications"""
        return self.APPLICATIONS
    
    def get_priorities(self):
        """Get available priority levels"""
        return self.PRIORITIES
    
    def get_time_ranges(self):
        """Get available time ranges"""
        return self.TIME_RANGES
