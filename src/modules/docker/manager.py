"""
Docker Manager Module

Provides Docker container monitoring and management functionality.
"""

import subprocess
import json
from typing import List, Dict, Optional, Any
from datetime import datetime


class DockerManager:
    """Manages Docker container operations and monitoring"""
    
    def __init__(self):
        """Initialize Docker manager"""
        self.docker_available = self._check_docker()
    
    def _check_docker(self) -> bool:
        """Check if Docker is installed and running"""
        try:
            result = subprocess.run(
                ['docker', 'info'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def _run_command(self, command: List[str]) -> Optional[str]:
        """Run a Docker command and return output"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except (subprocess.SubprocessError, FileNotFoundError):
            return None
    
    def get_containers(self, status: str = 'all') -> List[Dict[str, Any]]:
        """
        Get list of Docker containers
        
        Args:
            status: 'all', 'running', or 'stopped'
        
        Returns:
            List of container dictionaries
        """
        if not self.docker_available:
            return []
        
        cmd = ['docker', 'ps', '--format', '{{json .}}']
        
        if status == 'all':
            cmd.append('-a')
        elif status == 'stopped':
            cmd.extend(['-a', '--filter', 'status=exited'])
        
        output = self._run_command(cmd)
        if not output:
            return []
        
        containers = []
        for line in output.split('\n'):
            if line.strip():
                try:
                    container = json.loads(line)
                    containers.append({
                        'id': container.get('ID', '')[:12],
                        'name': container.get('Names', ''),
                        'image': container.get('Image', ''),
                        'status': container.get('State', ''),
                        'created': container.get('CreatedAt', ''),
                        'ports': container.get('Ports', '')
                    })
                except json.JSONDecodeError:
                    continue
        
        return containers
    
    def get_container_details(self, container_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a container
        
        Args:
            container_id: Container ID or name
        
        Returns:
            Dictionary with container details or None
        """
        if not self.docker_available:
            return None
        
        output = self._run_command(['docker', 'inspect', container_id])
        if not output:
            return None
        
        try:
            data = json.loads(output)
            if not data:
                return None
            
            container = data[0]
            state = container.get('State', {})
            config = container.get('Config', {})
            network = container.get('NetworkSettings', {})
            
            return {
                'id': container.get('Id', '')[:12],
                'name': container.get('Name', '').lstrip('/'),
                'image': config.get('Image', ''),
                'status': state.get('Status', ''),
                'running': state.get('Running', False),
                'created': container.get('Created', ''),
                'started': state.get('StartedAt', ''),
                'finished': state.get('FinishedAt', ''),
                'exit_code': state.get('ExitCode', 0),
                'ip_address': network.get('IPAddress', ''),
                'ports': self._format_ports(network.get('Ports', {})),
                'env': config.get('Env', []),
                'cmd': ' '.join(config.get('Cmd', [])) if config.get('Cmd') else ''
            }
        except (json.JSONDecodeError, KeyError, IndexError):
            return None
    
    def _format_ports(self, ports: Dict) -> str:
        """Format container ports for display"""
        if not ports:
            return 'None'
        
        port_list = []
        for container_port, host_bindings in ports.items():
            if host_bindings:
                for binding in host_bindings:
                    host_port = binding.get('HostPort', '')
                    if host_port:
                        port_list.append(f"{host_port}->{container_port}")
        
        return ', '.join(port_list) if port_list else 'None'
    
    def get_container_stats(self, container_id: str) -> Optional[Dict[str, Any]]:
        """
        Get real-time stats for a container
        
        Args:
            container_id: Container ID or name
        
        Returns:
            Dictionary with container stats or None
        """
        if not self.docker_available:
            return None
        
        output = self._run_command([
            'docker', 'stats', '--no-stream', '--format',
            '{{json .}}', container_id
        ])
        
        if not output:
            return None
        
        try:
            stats = json.loads(output)
            return {
                'cpu': stats.get('CPUPerc', '0%'),
                'memory': stats.get('MemUsage', '0B / 0B'),
                'memory_percent': stats.get('MemPerc', '0%'),
                'net_io': stats.get('NetIO', '0B / 0B'),
                'block_io': stats.get('BlockIO', '0B / 0B'),
                'pids': stats.get('PIDs', '0')
            }
        except (json.JSONDecodeError, KeyError):
            return None
    
    def get_container_logs(self, container_id: str, lines: int = 50) -> Optional[str]:
        """
        Get container logs
        
        Args:
            container_id: Container ID or name
            lines: Number of lines to retrieve (default: 50)
        
        Returns:
            Log content or None
        """
        if not self.docker_available:
            return None
        
        output = self._run_command([
            'docker', 'logs', '--tail', str(lines), container_id
        ])
        
        return output if output else 'No logs available'
    
    def start_container(self, container_id: str) -> bool:
        """Start a container"""
        if not self.docker_available:
            return False
        
        output = self._run_command(['docker', 'start', container_id])
        return output is not None
    
    def stop_container(self, container_id: str) -> bool:
        """Stop a container"""
        if not self.docker_available:
            return False
        
        output = self._run_command(['docker', 'stop', container_id])
        return output is not None
    
    def restart_container(self, container_id: str) -> bool:
        """Restart a container"""
        if not self.docker_available:
            return False
        
        output = self._run_command(['docker', 'restart', container_id])
        return output is not None
    
    def remove_container(self, container_id: str, force: bool = False) -> bool:
        """Remove a container"""
        if not self.docker_available:
            return False
        
        cmd = ['docker', 'rm', container_id]
        if force:
            cmd.insert(2, '-f')
        
        output = self._run_command(cmd)
        return output is not None
    
    def start_all_containers(self) -> int:
        """Start all stopped containers"""
        stopped = self.get_containers('stopped')
        count = 0
        for container in stopped:
            if self.start_container(container['id']):
                count += 1
        return count
    
    def stop_all_containers(self) -> int:
        """Stop all running containers"""
        running = self.get_containers('running')
        count = 0
        for container in running:
            if self.stop_container(container['id']):
                count += 1
        return count
    
    def remove_stopped_containers(self) -> int:
        """Remove all stopped containers"""
        stopped = self.get_containers('stopped')
        count = 0
        for container in stopped:
            if self.remove_container(container['id']):
                count += 1
        return count
    
    def format_container_list(self, containers: List[Dict[str, Any]]) -> str:
        """Format container list for Telegram display"""
        if not containers:
            return "No containers found."
        
        status_icons = {
            'running': '🟢',
            'exited': '🔴',
            'created': '🟡',
            'paused': '🟠',
            'restarting': '🔄'
        }
        
        lines = [f"🐳 <b>Docker Containers ({len(containers)})</b>\n"]
        
        for container in containers:
            status = container['status'].lower()
            icon = status_icons.get(status, '⚪')
            
            lines.append(
                f"{icon} <b>{container['name']}</b>\n"
                f"   ID: <code>{container['id']}</code>\n"
                f"   Image: {container['image']}\n"
                f"   Status: {container['status']}\n"
            )
        
        return '\n'.join(lines)
    
    def format_container_detail(self, details: Dict[str, Any]) -> str:
        """Format container details for Telegram display"""
        status_icon = '🟢' if details['running'] else '🔴'
        
        lines = [
            f"🐳 <b>Container Details</b>\n",
            f"{status_icon} <b>{details['name']}</b>",
            f"<b>ID:</b> <code>{details['id']}</code>",
            f"<b>Image:</b> {details['image']}",
            f"<b>Status:</b> {details['status']}",
            f"<b>Running:</b> {'Yes' if details['running'] else 'No'}",
            f"<b>IP Address:</b> {details['ip_address'] or 'N/A'}",
            f"<b>Ports:</b> {details['ports']}",
            f"<b>Created:</b> {details['created'][:19]}",
        ]
        
        if details['running']:
            lines.append(f"<b>Started:</b> {details['started'][:19]}")
        else:
            lines.append(f"<b>Finished:</b> {details['finished'][:19]}")
            lines.append(f"<b>Exit Code:</b> {details['exit_code']}")
        
        if details['cmd']:
            lines.append(f"<b>Command:</b> <code>{details['cmd']}</code>")
        
        return '\n'.join(lines)
    
    def format_container_stats(self, stats: Dict[str, Any], name: str) -> str:
        """Format container stats for Telegram display"""
        return (
            f"📊 <b>Container Stats: {name}</b>\n\n"
            f"<b>CPU:</b> {stats['cpu']}\n"
            f"<b>Memory:</b> {stats['memory']}\n"
            f"<b>Memory %:</b> {stats['memory_percent']}\n"
            f"<b>Network I/O:</b> {stats['net_io']}\n"
            f"<b>Block I/O:</b> {stats['block_io']}\n"
            f"<b>PIDs:</b> {stats['pids']}"
        )
