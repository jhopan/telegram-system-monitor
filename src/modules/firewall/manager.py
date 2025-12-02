"""
Firewall Manager Module

Provides UFW (Uncomplicated Firewall) management functionality.
"""

import subprocess
import re
from typing import List, Dict, Optional, Tuple


class FirewallManager:
    """Manages UFW firewall operations"""
    
    def __init__(self):
        """Initialize firewall manager"""
        self.ufw_available = self._check_ufw()
    
    def _check_ufw(self) -> bool:
        """Check if UFW is available"""
        try:
            result = subprocess.run(
                ['which', 'ufw'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def _run_command(self, command: List[str], timeout: int = 10) -> Tuple[bool, str]:
        """
        Run a command and return success status and output
        
        Returns:
            Tuple of (success, output)
        """
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return (result.returncode == 0, result.stdout + result.stderr)
        except subprocess.TimeoutExpired:
            return (False, "Command timed out")
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            return (False, str(e))
    
    def get_status(self) -> Dict[str, any]:
        """
        Get firewall status
        
        Returns:
            Dictionary with status info
        """
        if not self.ufw_available:
            return {'available': False}
        
        success, output = self._run_command(['sudo', 'ufw', 'status', 'verbose'])
        
        if not success:
            return {'available': True, 'enabled': False, 'error': output}
        
        # Parse output
        enabled = 'Status: active' in output
        
        # Extract default policies
        incoming = 'deny (incoming)' if 'deny (incoming)' in output else 'allow (incoming)' if 'allow (incoming)' in output else 'unknown'
        outgoing = 'allow (outgoing)' if 'allow (outgoing)' in output else 'deny (outgoing)' if 'deny (outgoing)' in output else 'unknown'
        routed = 'disabled (routed)' if 'disabled (routed)' in output else 'allow (routed)' if 'allow (routed)' in output else 'unknown'
        
        return {
            'available': True,
            'enabled': enabled,
            'default_incoming': incoming.split()[0],
            'default_outgoing': outgoing.split()[0],
            'default_routed': routed.split()[0]
        }
    
    def get_rules(self) -> List[Dict[str, str]]:
        """
        Get list of firewall rules
        
        Returns:
            List of rule dictionaries
        """
        if not self.ufw_available:
            return []
        
        success, output = self._run_command(['sudo', 'ufw', 'status', 'numbered'])
        
        if not success:
            return []
        
        rules = []
        for line in output.split('\n'):
            # Match lines like: [ 1] 22/tcp                     ALLOW IN    Anywhere
            match = re.match(r'\[\s*(\d+)\]\s+(.+?)\s+(ALLOW|DENY|REJECT|LIMIT)\s+(IN|OUT)\s+(.+)', line)
            if match:
                rules.append({
                    'number': match.group(1),
                    'port_proto': match.group(2).strip(),
                    'action': match.group(3),
                    'direction': match.group(4),
                    'from': match.group(5).strip()
                })
        
        return rules
    
    def enable(self) -> Tuple[bool, str]:
        """
        Enable firewall
        
        Returns:
            Tuple of (success, message)
        """
        if not self.ufw_available:
            return (False, "UFW not available")
        
        # Use --force to avoid interactive prompt
        success, output = self._run_command(['sudo', 'ufw', '--force', 'enable'])
        
        if success:
            return (True, "Firewall enabled successfully!")
        else:
            return (False, f"Failed to enable firewall.\n{output[:500]}")
    
    def disable(self) -> Tuple[bool, str]:
        """
        Disable firewall
        
        Returns:
            Tuple of (success, message)
        """
        if not self.ufw_available:
            return (False, "UFW not available")
        
        success, output = self._run_command(['sudo', 'ufw', 'disable'])
        
        if success:
            return (True, "Firewall disabled successfully!")
        else:
            return (False, f"Failed to disable firewall.\n{output[:500]}")
    
    def add_rule(self, port: str, protocol: str = 'tcp', action: str = 'allow') -> Tuple[bool, str]:
        """
        Add a firewall rule
        
        Args:
            port: Port number or service name
            protocol: tcp or udp (default: tcp)
            action: allow, deny, reject, or limit (default: allow)
        
        Returns:
            Tuple of (success, message)
        """
        if not self.ufw_available:
            return (False, "UFW not available")
        
        cmd = ['sudo', 'ufw', action, f'{port}/{protocol}']
        success, output = self._run_command(cmd)
        
        if success or 'Rule added' in output or 'Rules updated' in output:
            return (True, f"Rule added: {action} {port}/{protocol}")
        else:
            return (False, f"Failed to add rule.\n{output[:500]}")
    
    def delete_rule(self, rule_number: str) -> Tuple[bool, str]:
        """
        Delete a firewall rule by number
        
        Args:
            rule_number: Rule number from status numbered output
        
        Returns:
            Tuple of (success, message)
        """
        if not self.ufw_available:
            return (False, "UFW not available")
        
        # Use --force to avoid interactive prompt
        success, output = self._run_command(['sudo', 'ufw', '--force', 'delete', rule_number])
        
        if success or 'Deleting' in output:
            return (True, f"Rule #{rule_number} deleted successfully!")
        else:
            return (False, f"Failed to delete rule.\n{output[:500]}")
    
    def reset(self) -> Tuple[bool, str]:
        """
        Reset firewall to default settings
        
        Returns:
            Tuple of (success, message)
        """
        if not self.ufw_available:
            return (False, "UFW not available")
        
        # Use --force to avoid interactive prompt
        success, output = self._run_command(['sudo', 'ufw', '--force', 'reset'])
        
        if success:
            return (True, "Firewall reset to default settings!")
        else:
            return (False, f"Failed to reset firewall.\n{output[:500]}")
    
    def set_default_policy(self, direction: str, policy: str) -> Tuple[bool, str]:
        """
        Set default policy
        
        Args:
            direction: incoming, outgoing, or routed
            policy: allow, deny, or reject
        
        Returns:
            Tuple of (success, message)
        """
        if not self.ufw_available:
            return (False, "UFW not available")
        
        cmd = ['sudo', 'ufw', 'default', policy, direction]
        success, output = self._run_command(cmd)
        
        if success:
            return (True, f"Default {direction} policy set to {policy}!")
        else:
            return (False, f"Failed to set policy.\n{output[:500]}")
    
    def format_status(self, status: Dict[str, any]) -> str:
        """Format firewall status for Telegram display"""
        if not status.get('available'):
            return "❌ <b>UFW Not Available</b>\n\nUFW is not installed on this system."
        
        if status.get('error'):
            return f"❌ <b>Error</b>\n\n{status['error']}"
        
        enabled = status.get('enabled', False)
        status_icon = "🟢" if enabled else "🔴"
        status_text = "Active" if enabled else "Inactive"
        
        default_in = status.get('default_incoming', 'unknown')
        default_out = status.get('default_outgoing', 'unknown')
        
        in_icon = "🔒" if default_in == 'deny' else "🔓"
        out_icon = "🔒" if default_out == 'deny' else "🔓"
        
        return (
            f"🛡️ <b>Firewall Status</b>\n\n"
            f"{status_icon} <b>Status:</b> {status_text}\n\n"
            f"<b>Default Policies:</b>\n"
            f"{in_icon} Incoming: <code>{default_in}</code>\n"
            f"{out_icon} Outgoing: <code>{default_out}</code>"
        )
    
    def format_rules(self, rules: List[Dict[str, str]]) -> str:
        """Format firewall rules for Telegram display"""
        if not rules:
            return "🛡️ <b>Firewall Rules</b>\n\nNo rules configured."
        
        lines = [f"🛡️ <b>Firewall Rules ({len(rules)})</b>\n"]
        
        for rule in rules:
            action_icon = "✅" if rule['action'] == 'ALLOW' else "❌" if rule['action'] == 'DENY' else "⚠️"
            direction = "⬇️" if rule['direction'] == 'IN' else "⬆️"
            
            lines.append(
                f"{action_icon} <b>Rule #{rule['number']}</b>\n"
                f"   {direction} {rule['port_proto']} - {rule['action']}\n"
                f"   From: {rule['from']}\n"
            )
        
        return '\n'.join(lines)
    
    # Preset services for easy rule management
    PRESET_SERVICES = {
        'ssh': {'port': '22', 'protocol': 'tcp', 'name': 'SSH'},
        'http': {'port': '80', 'protocol': 'tcp', 'name': 'HTTP'},
        'https': {'port': '443', 'protocol': 'tcp', 'name': 'HTTPS'},
        'ftp': {'port': '21', 'protocol': 'tcp', 'name': 'FTP'},
        'mysql': {'port': '3306', 'protocol': 'tcp', 'name': 'MySQL'},
        'postgresql': {'port': '5432', 'protocol': 'tcp', 'name': 'PostgreSQL'},
        'mongodb': {'port': '27017', 'protocol': 'tcp', 'name': 'MongoDB'},
        'redis': {'port': '6379', 'protocol': 'tcp', 'name': 'Redis'},
        'smtp': {'port': '25', 'protocol': 'tcp', 'name': 'SMTP'},
        'dns': {'port': '53', 'protocol': 'udp', 'name': 'DNS'},
        'ntp': {'port': '123', 'protocol': 'udp', 'name': 'NTP'},
        'docker': {'port': '2375', 'protocol': 'tcp', 'name': 'Docker'},
    }
    
    def get_preset_services(self) -> Dict[str, Dict[str, str]]:
        """Get preset services"""
        return self.PRESET_SERVICES
