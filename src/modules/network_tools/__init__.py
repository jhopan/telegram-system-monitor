"""
Advanced Network Tools Module

Provides comprehensive network diagnostic and testing tools.
"""

import subprocess
import socket
import time
from typing import List, Dict, Optional, Tuple
import re


class NetworkTools:
    """Advanced network diagnostic tools"""
    
    def __init__(self):
        """Initialize network tools"""
        pass
    
    def _run_command(self, command: List[str], timeout: int = 30) -> Tuple[bool, str]:
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
    
    def ping_host(self, host: str, count: int = 4) -> Dict:
        """
        Ping a host
        
        Args:
            host: Hostname or IP address
            count: Number of ping packets
        
        Returns:
            Dict with ping results
        """
        cmd = ['ping', '-c', str(count), host]
        success, output = self._run_command(cmd, timeout=count * 5)
        
        result = {
            'host': host,
            'success': success,
            'output': output,
            'packet_loss': None,
            'avg_time': None,
            'min_time': None,
            'max_time': None
        }
        
        if success:
            # Parse statistics
            loss_match = re.search(r'(\d+)% packet loss', output)
            if loss_match:
                result['packet_loss'] = int(loss_match.group(1))
            
            # Parse timing (min/avg/max)
            time_match = re.search(r'min/avg/max[^=]*=\s*([\d.]+)/([\d.]+)/([\d.]+)', output)
            if time_match:
                result['min_time'] = float(time_match.group(1))
                result['avg_time'] = float(time_match.group(2))
                result['max_time'] = float(time_match.group(3))
        
        return result
    
    def traceroute(self, host: str, max_hops: int = 30) -> Dict:
        """
        Traceroute to a host
        
        Args:
            host: Hostname or IP address
            max_hops: Maximum number of hops
        
        Returns:
            Dict with traceroute results
        """
        cmd = ['traceroute', '-m', str(max_hops), host]
        success, output = self._run_command(cmd, timeout=60)
        
        return {
            'host': host,
            'success': success,
            'output': output,
            'hops': output.count('\n') if success else 0
        }
    
    def port_scan(self, host: str, port: int, timeout: float = 2.0) -> Dict:
        """
        Scan a single port
        
        Args:
            host: Hostname or IP address
            port: Port number
            timeout: Connection timeout
        
        Returns:
            Dict with scan result
        """
        result = {
            'host': host,
            'port': port,
            'open': False,
            'service': None
        }
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result['open'] = (sock.connect_ex((host, port)) == 0)
            sock.close()
            
            if result['open']:
                try:
                    result['service'] = socket.getservbyport(port)
                except:
                    pass
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def port_scan_range(self, host: str, start_port: int, end_port: int, timeout: float = 1.0) -> List[Dict]:
        """
        Scan a range of ports
        
        Args:
            host: Hostname or IP address
            start_port: Starting port
            end_port: Ending port
            timeout: Connection timeout per port
        
        Returns:
            List of open ports
        """
        open_ports = []
        
        for port in range(start_port, end_port + 1):
            result = self.port_scan(host, port, timeout)
            if result['open']:
                open_ports.append(result)
        
        return open_ports
    
    def dns_lookup(self, domain: str, record_type: str = 'A') -> Dict:
        """
        DNS lookup
        
        Args:
            domain: Domain name
            record_type: Record type (A, AAAA, MX, NS, TXT)
        
        Returns:
            Dict with DNS results
        """
        cmd = ['dig', '+short', domain, record_type]
        success, output = self._run_command(cmd, timeout=10)
        
        records = []
        if success and output.strip():
            records = [line.strip() for line in output.strip().split('\n') if line.strip()]
        
        return {
            'domain': domain,
            'type': record_type,
            'success': success,
            'records': records,
            'count': len(records)
        }
    
    def whois_lookup(self, domain: str) -> Dict:
        """
        Whois lookup
        
        Args:
            domain: Domain name or IP
        
        Returns:
            Dict with whois results
        """
        cmd = ['whois', domain]
        success, output = self._run_command(cmd, timeout=15)
        
        return {
            'domain': domain,
            'success': success,
            'output': output
        }
    
    def resolve_hostname(self, hostname: str) -> Dict:
        """
        Resolve hostname to IP
        
        Args:
            hostname: Hostname to resolve
        
        Returns:
            Dict with resolution results
        """
        result = {
            'hostname': hostname,
            'success': False,
            'ip': None,
            'error': None
        }
        
        try:
            result['ip'] = socket.gethostbyname(hostname)
            result['success'] = True
        except socket.gaierror as e:
            result['error'] = str(e)
        
        return result
    
    def check_port(self, host: str, port: int) -> bool:
        """Quick check if port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port)) == 0
            sock.close()
            return result
        except:
            return False
    
    def format_ping_result(self, result: Dict) -> str:
        """Format ping result for display"""
        if not result['success']:
            return f"❌ Ping to {result['host']} failed:\n{result['output'][:500]}"
        
        output = f"🏓 <b>Ping: {result['host']}</b>\n\n"
        
        if result['packet_loss'] is not None:
            icon = "✅" if result['packet_loss'] == 0 else "⚠️" if result['packet_loss'] < 50 else "❌"
            output += f"{icon} <b>Packet Loss:</b> {result['packet_loss']}%\n"
        
        if result['avg_time'] is not None:
            output += f"⏱️ <b>Average Time:</b> {result['avg_time']:.2f} ms\n"
            output += f"📊 <b>Min/Max:</b> {result['min_time']:.2f} / {result['max_time']:.2f} ms\n"
        
        return output
    
    def format_traceroute_result(self, result: Dict, max_lines: int = 20) -> str:
        """Format traceroute result for display"""
        if not result['success']:
            return f"❌ Traceroute to {result['host']} failed:\n{result['output'][:500]}"
        
        output = f"🛤️ <b>Traceroute: {result['host']}</b>\n\n"
        
        lines = result['output'].strip().split('\n')[:max_lines]
        output += f"<pre>{chr(10).join(lines)}</pre>\n\n"
        
        if result['hops'] > max_lines:
            output += f"<i>... showing first {max_lines} of {result['hops']} hops ...</i>"
        else:
            output += f"<i>Total hops: {result['hops']}</i>"
        
        return output
    
    def format_dns_result(self, result: Dict) -> str:
        """Format DNS lookup result for display"""
        if not result['success'] or not result['records']:
            return f"❌ No {result['type']} records found for {result['domain']}"
        
        output = f"🔍 <b>DNS Lookup: {result['domain']}</b>\n"
        output += f"📝 <b>Type:</b> {result['type']}\n"
        output += f"📊 <b>Records:</b> {result['count']}\n\n"
        
        for i, record in enumerate(result['records'][:10], 1):
            output += f"{i}. <code>{record}</code>\n"
        
        if result['count'] > 10:
            output += f"\n<i>... showing first 10 of {result['count']} records ...</i>"
        
        return output
    
    # Common hosts for quick testing
    COMMON_HOSTS = {
        'dns': {
            'google_dns': {'name': '🌐 Google DNS', 'host': '8.8.8.8'},
            'cloudflare_dns': {'name': '☁️ Cloudflare DNS', 'host': '1.1.1.1'},
            'quad9': {'name': '🛡️ Quad9 DNS', 'host': '9.9.9.9'}
        },
        'websites': {
            'google': {'name': '🔍 Google', 'host': 'google.com'},
            'github': {'name': '🐙 GitHub', 'host': 'github.com'},
            'cloudflare': {'name': '☁️ Cloudflare', 'host': 'cloudflare.com'}
        },
        'local': {
            'localhost': {'name': '🏠 Localhost', 'host': '127.0.0.1'},
            'gateway': {'name': '🚪 Gateway', 'host': '192.168.1.1'},
            'router': {'name': '📡 Router', 'host': '192.168.0.1'}
        }
    }
    
    # Common ports for scanning
    COMMON_PORTS = {
        'web': {
            'http': {'name': '🌐 HTTP', 'port': 80},
            'https': {'name': '🔒 HTTPS', 'port': 443},
            'http_alt': {'name': '🌐 HTTP Alt', 'port': 8080}
        },
        'remote': {
            'ssh': {'name': '🔐 SSH', 'port': 22},
            'telnet': {'name': '📟 Telnet', 'port': 23},
            'rdp': {'name': '🖥️ RDP', 'port': 3389}
        },
        'database': {
            'mysql': {'name': '🗄️ MySQL', 'port': 3306},
            'postgresql': {'name': '🐘 PostgreSQL', 'port': 5432},
            'mongodb': {'name': '🍃 MongoDB', 'port': 27017},
            'redis': {'name': '📦 Redis', 'port': 6379}
        },
        'mail': {
            'smtp': {'name': '📧 SMTP', 'port': 25},
            'pop3': {'name': '📬 POP3', 'port': 110},
            'imap': {'name': '📮 IMAP', 'port': 143}
        },
        'other': {
            'ftp': {'name': '📁 FTP', 'port': 21},
            'dns': {'name': '🌐 DNS', 'port': 53},
            'ntp': {'name': '🕐 NTP', 'port': 123}
        }
    }
    
    DNS_RECORD_TYPES = {
        'A': '🌐 IPv4 Address',
        'AAAA': '🌐 IPv6 Address',
        'MX': '📧 Mail Exchange',
        'NS': '🌐 Name Server',
        'TXT': '📝 Text Record',
        'CNAME': '🔗 Canonical Name'
    }
    
    def get_common_hosts(self):
        """Get common hosts dictionary"""
        return self.COMMON_HOSTS
    
    def get_common_ports(self):
        """Get common ports dictionary"""
        return self.COMMON_PORTS
    
    def get_dns_record_types(self):
        """Get DNS record types"""
        return self.DNS_RECORD_TYPES
