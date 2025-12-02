"""
Package Manager Module

Provides APT package management functionality for Debian/Ubuntu systems.
"""

import subprocess
import re
from typing import List, Dict, Optional, Tuple


class PackageManager:
    """Manages APT package operations"""
    
    def __init__(self):
        """Initialize package manager"""
        self.apt_available = self._check_apt()
    
    def _check_apt(self) -> bool:
        """Check if APT is available"""
        try:
            result = subprocess.run(
                ['apt', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def _run_command(self, command: List[str], timeout: int = 30) -> Tuple[bool, str]:
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
    
    def get_installed_packages(self, limit: int = 50) -> List[Dict[str, str]]:
        """
        Get list of installed packages
        
        Args:
            limit: Maximum number of packages to return
        
        Returns:
            List of package dictionaries
        """
        if not self.apt_available:
            return []
        
        success, output = self._run_command(['dpkg', '-l'])
        if not success:
            return []
        
        packages = []
        for line in output.split('\n'):
            if line.startswith('ii'):
                parts = line.split()
                if len(parts) >= 4:
                    packages.append({
                        'name': parts[1],
                        'version': parts[2],
                        'arch': parts[3] if len(parts) > 3 else '',
                        'description': ' '.join(parts[4:]) if len(parts) > 4 else ''
                    })
        
        return packages[:limit]
    
    def search_packages(self, query: str) -> List[Dict[str, str]]:
        """
        Search for packages
        
        Args:
            query: Search query
        
        Returns:
            List of matching packages
        """
        if not self.apt_available:
            return []
        
        success, output = self._run_command(['apt-cache', 'search', query])
        if not success:
            return []
        
        packages = []
        for line in output.split('\n')[:20]:  # Limit to 20 results
            if ' - ' in line:
                name, description = line.split(' - ', 1)
                packages.append({
                    'name': name.strip(),
                    'description': description.strip()
                })
        
        return packages
    
    def get_package_info(self, package_name: str) -> Optional[Dict[str, str]]:
        """
        Get detailed information about a package
        
        Args:
            package_name: Name of the package
        
        Returns:
            Dictionary with package info or None
        """
        if not self.apt_available:
            return None
        
        success, output = self._run_command(['apt-cache', 'show', package_name])
        if not success:
            return None
        
        info = {}
        for line in output.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                info[key.strip()] = value.strip()
        
        return info
    
    def is_package_installed(self, package_name: str) -> bool:
        """Check if a package is installed"""
        success, output = self._run_command(['dpkg', '-l', package_name])
        return success and 'ii' in output
    
    def get_upgradeable_packages(self) -> List[Dict[str, str]]:
        """
        Get list of upgradeable packages
        
        Returns:
            List of upgradeable packages
        """
        if not self.apt_available:
            return []
        
        success, output = self._run_command(['apt', 'list', '--upgradable'])
        if not success:
            return []
        
        packages = []
        for line in output.split('\n'):
            if '/' in line and '[upgradable' in line:
                parts = line.split()
                if len(parts) >= 2:
                    name = parts[0].split('/')[0]
                    version = parts[1] if len(parts) > 1 else ''
                    packages.append({
                        'name': name,
                        'version': version,
                        'current': parts[5] if len(parts) > 5 else ''
                    })
        
        return packages
    
    def update_package_list(self) -> Tuple[bool, str]:
        """
        Update package list (apt update)
        
        Returns:
            Tuple of (success, message)
        """
        if not self.apt_available:
            return (False, "APT not available")
        
        success, output = self._run_command(['sudo', 'apt', 'update'], timeout=60)
        
        if success:
            # Parse output for summary
            lines = output.split('\n')
            summary = '\n'.join([l for l in lines if 'packages' in l.lower() or 'updated' in l.lower()])
            return (True, f"Package list updated successfully!\n\n{summary}")
        else:
            return (False, f"Failed to update package list.\n{output[:500]}")
    
    def upgrade_packages(self, package_name: Optional[str] = None) -> Tuple[bool, str]:
        """
        Upgrade packages (apt upgrade)
        
        Args:
            package_name: Specific package to upgrade, or None for all
        
        Returns:
            Tuple of (success, message)
        """
        if not self.apt_available:
            return (False, "APT not available")
        
        if package_name:
            cmd = ['sudo', 'apt', 'install', '--only-upgrade', '-y', package_name]
        else:
            cmd = ['sudo', 'apt', 'upgrade', '-y']
        
        success, output = self._run_command(cmd, timeout=300)
        
        if success:
            return (True, "Packages upgraded successfully!")
        else:
            return (False, f"Failed to upgrade packages.\n{output[:500]}")
    
    def install_package(self, package_name: str) -> Tuple[bool, str]:
        """
        Install a package
        
        Args:
            package_name: Name of the package to install
        
        Returns:
            Tuple of (success, message)
        """
        if not self.apt_available:
            return (False, "APT not available")
        
        success, output = self._run_command(
            ['sudo', 'apt', 'install', '-y', package_name],
            timeout=300
        )
        
        if success:
            return (True, f"Package '{package_name}' installed successfully!")
        else:
            return (False, f"Failed to install '{package_name}'.\n{output[:500]}")
    
    def remove_package(self, package_name: str) -> Tuple[bool, str]:
        """
        Remove a package
        
        Args:
            package_name: Name of the package to remove
        
        Returns:
            Tuple of (success, message)
        """
        if not self.apt_available:
            return (False, "APT not available")
        
        success, output = self._run_command(
            ['sudo', 'apt', 'remove', '-y', package_name],
            timeout=120
        )
        
        if success:
            return (True, f"Package '{package_name}' removed successfully!")
        else:
            return (False, f"Failed to remove '{package_name}'.\n{output[:500]}")
    
    def autoremove(self) -> Tuple[bool, str]:
        """
        Remove unused packages (apt autoremove)
        
        Returns:
            Tuple of (success, message)
        """
        if not self.apt_available:
            return (False, "APT not available")
        
        success, output = self._run_command(['sudo', 'apt', 'autoremove', '-y'], timeout=120)
        
        if success:
            return (True, "Unused packages removed successfully!")
        else:
            return (False, f"Failed to autoremove.\n{output[:500]}")
    
    def get_package_count(self) -> Dict[str, int]:
        """Get package statistics"""
        if not self.apt_available:
            return {'installed': 0, 'upgradeable': 0}
        
        # Count installed
        success, output = self._run_command(['dpkg', '-l'])
        installed = len([l for l in output.split('\n') if l.startswith('ii')])
        
        # Count upgradeable
        upgradeable = len(self.get_upgradeable_packages())
        
        return {
            'installed': installed,
            'upgradeable': upgradeable
        }
    
    def format_package_list(self, packages: List[Dict[str, str]], title: str = "Packages") -> str:
        """Format package list for Telegram display"""
        if not packages:
            return f"📦 <b>{title}</b>\n\nNo packages found."
        
        lines = [f"📦 <b>{title} ({len(packages)})</b>\n"]
        
        for pkg in packages[:20]:  # Limit to 20
            name = pkg.get('name', 'Unknown')
            version = pkg.get('version', '')
            desc = pkg.get('description', '')[:50]  # Truncate description
            
            lines.append(f"• <b>{name}</b>")
            if version:
                lines.append(f"  Version: <code>{version}</code>")
            if desc:
                lines.append(f"  {desc}...")
            lines.append("")
        
        if len(packages) > 20:
            lines.append(f"<i>... and {len(packages) - 20} more packages</i>")
        
        return '\n'.join(lines)
    
    def format_package_info(self, info: Dict[str, str]) -> str:
        """Format package info for Telegram display"""
        if not info:
            return "❌ Package information not available."
        
        package = info.get('Package', 'Unknown')
        version = info.get('Version', 'Unknown')
        section = info.get('Section', 'Unknown')
        priority = info.get('Priority', 'Unknown')
        installed_size = info.get('Installed-Size', 'Unknown')
        maintainer = info.get('Maintainer', 'Unknown')
        description = info.get('Description', 'No description')[:200]
        
        return (
            f"📦 <b>Package Information</b>\n\n"
            f"<b>Name:</b> {package}\n"
            f"<b>Version:</b> <code>{version}</code>\n"
            f"<b>Section:</b> {section}\n"
            f"<b>Priority:</b> {priority}\n"
            f"<b>Size:</b> {installed_size} KB\n"
            f"<b>Maintainer:</b> {maintainer}\n\n"
            f"<b>Description:</b>\n{description}"
        )
    
    # Preset package categories for easy installation
    PRESET_PACKAGES = {
        'webserver': {
            'nginx': 'High-performance web server',
            'apache2': 'Apache HTTP Server',
            'lighttpd': 'Lightweight web server'
        },
        'database': {
            'mysql-server': 'MySQL database server',
            'postgresql': 'PostgreSQL database',
            'mongodb': 'MongoDB NoSQL database',
            'redis-server': 'Redis in-memory database'
        },
        'devtools': {
            'git': 'Version control system',
            'curl': 'Command-line tool for transferring data',
            'wget': 'Network downloader',
            'vim': 'Advanced text editor',
            'build-essential': 'Essential build tools'
        },
        'monitoring': {
            'htop': 'Interactive process viewer',
            'iotop': 'I/O monitoring',
            'nethogs': 'Network monitoring per process',
            'vnstat': 'Network traffic monitor'
        },
        'system': {
            'ufw': 'Uncomplicated Firewall',
            'fail2ban': 'Intrusion prevention',
            'unattended-upgrades': 'Automatic security updates',
            'cron': 'Task scheduler'
        }
    }
    
    def get_preset_categories(self) -> List[str]:
        """Get list of preset categories"""
        return list(self.PRESET_PACKAGES.keys())
    
    def get_preset_packages(self, category: str) -> Dict[str, str]:
        """Get preset packages for a category"""
        return self.PRESET_PACKAGES.get(category, {})
