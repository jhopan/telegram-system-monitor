"""
Scripts Manager Module

Provides custom bash script execution functionality.
"""

import subprocess
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from pathlib import Path


class ScriptsManager:
    """Manages custom script execution"""
    
    def __init__(self):
        """Initialize scripts manager"""
        self.history_file = Path.home() / '.telegram_bot' / 'script_history.json'
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
    
    def execute_script(self, script: str, timeout: int = 30) -> Tuple[bool, str, str]:
        """
        Execute a bash script
        
        Args:
            script: Script content
            timeout: Timeout in seconds
        
        Returns:
            Tuple of (success, stdout, stderr)
        """
        try:
            result = subprocess.run(
                ['bash', '-c', script],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            success = result.returncode == 0
            return (success, result.stdout, result.stderr)
        
        except subprocess.TimeoutExpired:
            return (False, "", "Script execution timed out")
        except Exception as e:
            return (False, "", str(e))
    
    def save_to_history(self, script_name: str, category: str, success: bool, output: str) -> None:
        """Save script execution to history"""
        try:
            history = self.get_history()
            
            entry = {
                'name': script_name,
                'category': category,
                'success': success,
                'output': output[:500],  # Limit output size
                'timestamp': datetime.now().isoformat()
            }
            
            history.insert(0, entry)
            history = history[:50]  # Keep last 50 executions
            
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception:
            pass  # Silently fail if history can't be saved
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """Get script execution history"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
                    return history[:limit]
        except Exception:
            pass
        return []
    
    def clear_history(self) -> bool:
        """Clear script execution history"""
        try:
            if self.history_file.exists():
                self.history_file.unlink()
            return True
        except Exception:
            return False
    
    def format_output(self, output: str, max_length: int = 3000) -> str:
        """Format script output for Telegram"""
        if not output:
            return "<i>No output</i>"
        
        if len(output) > max_length:
            output = output[:max_length] + "\n\n<i>... output truncated ...</i>"
        
        return f"<pre>{output}</pre>"
    
    def format_history(self, history: List[Dict]) -> str:
        """Format script history for Telegram"""
        if not history:
            return "📜 <b>Script History</b>\n\nNo scripts executed yet."
        
        lines = [f"📜 <b>Script History (Last {len(history)})</b>\n"]
        
        for entry in history:
            icon = "✅" if entry.get('success') else "❌"
            name = entry.get('name', 'Unknown')
            category = entry.get('category', 'Unknown')
            timestamp = entry.get('timestamp', '')[:19]
            
            lines.append(
                f"{icon} <b>{name}</b>\n"
                f"   Category: {category}\n"
                f"   Time: {timestamp}\n"
            )
        
        return '\n'.join(lines)
    
    # Preset scripts organized by category
    PRESET_SCRIPTS = {
        'system': {
            'sysinfo': {
                'name': 'System Information',
                'description': 'Detailed system information',
                'script': '''
                    echo "=== System Information ==="
                    echo ""
                    echo "Hostname: $(hostname)"
                    echo "Kernel: $(uname -r)"
                    echo "OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
                    echo "Uptime: $(uptime -p)"
                    echo ""
                    echo "=== CPU Info ==="
                    lscpu | grep -E "Model name|CPU\\(s\\)|Thread|Core"
                    echo ""
                    echo "=== Memory Info ==="
                    free -h
                    echo ""
                    echo "=== Disk Usage ==="
                    df -h | grep -E "^/dev"
                '''
            },
            'users_logged': {
                'name': 'Logged In Users',
                'description': 'Show currently logged in users',
                'script': 'w'
            },
            'last_logins': {
                'name': 'Last Logins',
                'description': 'Show last 10 login attempts',
                'script': 'last -n 10'
            },
            'top_processes': {
                'name': 'Top Processes',
                'description': 'Top 10 processes by CPU',
                'script': 'ps aux --sort=-%cpu | head -11'
            }
        },
        'cleanup': {
            'apt_clean': {
                'name': 'APT Clean',
                'description': 'Clean APT cache',
                'script': 'sudo apt clean && sudo apt autoclean && echo "APT cache cleaned"'
            },
            'remove_old_kernels': {
                'name': 'Remove Old Kernels',
                'description': 'Remove old kernel versions',
                'script': 'sudo apt autoremove --purge -y && echo "Old kernels removed"'
            },
            'clear_logs': {
                'name': 'Clear Old Logs',
                'description': 'Clear logs older than 7 days',
                'script': 'sudo journalctl --vacuum-time=7d && echo "Old logs cleared"'
            },
            'clear_tmp': {
                'name': 'Clear /tmp',
                'description': 'Clear temporary files',
                'script': 'sudo rm -rf /tmp/* && echo "/tmp cleared"'
            }
        },
        'backup': {
            'backup_etc': {
                'name': 'Backup /etc',
                'description': 'Backup /etc directory',
                'script': '''
                    BACKUP_FILE="/root/etc-backup-$(date +%Y%m%d).tar.gz"
                    sudo tar -czf "$BACKUP_FILE" /etc 2>/dev/null
                    echo "Backup created: $BACKUP_FILE"
                    ls -lh "$BACKUP_FILE"
                '''
            },
            'list_backups': {
                'name': 'List Backups',
                'description': 'List all backup files',
                'script': 'ls -lh /root/*backup*.tar.gz 2>/dev/null || echo "No backups found"'
            },
            'backup_cron': {
                'name': 'Backup Crontab',
                'description': 'Backup crontab entries',
                'script': '''
                    BACKUP_FILE="/root/crontab-backup-$(date +%Y%m%d).txt"
                    crontab -l > "$BACKUP_FILE" 2>/dev/null
                    echo "Crontab backed up to: $BACKUP_FILE"
                    cat "$BACKUP_FILE"
                '''
            }
        },
        'network': {
            'network_info': {
                'name': 'Network Overview',
                'description': 'Network interfaces and stats',
                'script': '''
                    echo "=== Network Interfaces ==="
                    ip -br addr
                    echo ""
                    echo "=== Active Connections ==="
                    netstat -tuln | head -15
                '''
            },
            'check_ports': {
                'name': 'Open Ports',
                'description': 'List all listening ports',
                'script': 'sudo netstat -tulpn | grep LISTEN'
            },
            'ping_test': {
                'name': 'Ping Test',
                'description': 'Test connectivity to common sites',
                'script': '''
                    for host in google.com cloudflare.com 8.8.8.8; do
                        echo "Ping $host:"
                        ping -c 3 $host | tail -2
                        echo ""
                    done
                '''
            },
            'dns_check': {
                'name': 'DNS Check',
                'description': 'Check DNS configuration',
                'script': '''
                    echo "=== DNS Servers ==="
                    cat /etc/resolv.conf | grep nameserver
                    echo ""
                    echo "=== DNS Test ==="
                    nslookup google.com
                '''
            }
        },
        'performance': {
            'load_average': {
                'name': 'Load Average',
                'description': 'System load statistics',
                'script': '''
                    echo "=== Load Average ==="
                    uptime
                    echo ""
                    echo "=== CPU Usage ==="
                    mpstat 1 3 2>/dev/null || top -bn1 | grep "Cpu(s)"
                '''
            },
            'memory_top': {
                'name': 'Memory Hogs',
                'description': 'Top 10 memory-consuming processes',
                'script': 'ps aux --sort=-%mem | head -11'
            },
            'io_stats': {
                'name': 'I/O Statistics',
                'description': 'Disk I/O statistics',
                'script': 'iostat -x 1 3 2>/dev/null || echo "iostat not installed"'
            },
            'network_bandwidth': {
                'name': 'Network Bandwidth',
                'description': 'Network usage by interface',
                'script': '''
                    echo "=== Network Statistics ==="
                    for iface in $(ls /sys/class/net/ | grep -v lo); do
                        echo "$iface:"
                        cat /sys/class/net/$iface/statistics/rx_bytes | awk '{print "  RX: " $1/1024/1024 " MB"}'
                        cat /sys/class/net/$iface/statistics/tx_bytes | awk '{print "  TX: " $1/1024/1024 " MB"}'
                    done
                '''
            }
        }
    }
    
    def get_categories(self) -> Dict[str, str]:
        """Get script categories"""
        return {
            'system': '🖥️ System Info',
            'cleanup': '🧹 Cleanup',
            'backup': '💾 Backup',
            'network': '🌐 Network',
            'performance': '⚡ Performance'
        }
    
    def get_scripts_by_category(self, category: str) -> Dict[str, Dict]:
        """Get scripts for a category"""
        return self.PRESET_SCRIPTS.get(category, {})
    
    def get_script(self, category: str, script_id: str) -> Optional[Dict]:
        """Get a specific script"""
        scripts = self.get_scripts_by_category(category)
        return scripts.get(script_id)
