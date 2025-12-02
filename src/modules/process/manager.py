"""
Process Manager
Advanced process operations
"""
import psutil
from typing import List, Dict, Optional
import signal


class ProcessManager:
    """Manage system processes"""
    
    def __init__(self):
        self.cached_processes = []
        self.last_update = 0
    
    def get_all_processes(self, sort_by='cpu', limit=20) -> List[Dict]:
        """Get all processes sorted by criteria"""
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status', 'create_time']):
                try:
                    info = proc.info
                    # Get CPU percent (will be 0.0 on first call)
                    info['cpu_percent'] = proc.cpu_percent(interval=0.1)
                    processes.append(info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort
            if sort_by == 'cpu':
                processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            elif sort_by == 'memory':
                processes.sort(key=lambda x: x.get('memory_percent', 0), reverse=True)
            elif sort_by == 'name':
                processes.sort(key=lambda x: x.get('name', '').lower())
            elif sort_by == 'pid':
                processes.sort(key=lambda x: x.get('pid', 0))
            
            return processes[:limit]
        
        except Exception as e:
            return []
    
    def search_processes(self, query: str) -> List[Dict]:
        """Search processes by name"""
        try:
            query_lower = query.lower()
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    info = proc.info
                    if query_lower in info['name'].lower():
                        info['cpu_percent'] = proc.cpu_percent(interval=0.1)
                        processes.append(info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return processes[:20]
        
        except Exception as e:
            return []
    
    def filter_by_user(self, username: str) -> List[Dict]:
        """Filter processes by username"""
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    info = proc.info
                    if info.get('username') == username:
                        info['cpu_percent'] = proc.cpu_percent(interval=0.1)
                        processes.append(info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return processes[:20]
        
        except Exception as e:
            return []
    
    def filter_by_status(self, status: str) -> List[Dict]:
        """Filter processes by status (running, sleeping, etc)"""
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    info = proc.info
                    if info.get('status', '').lower() == status.lower():
                        info['cpu_percent'] = proc.cpu_percent(interval=0.1)
                        processes.append(info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return processes[:20]
        
        except Exception as e:
            return []
    
    def get_process_info(self, pid: int) -> Optional[Dict]:
        """Get detailed info for specific process"""
        try:
            proc = psutil.Process(pid)
            
            info = {
                'pid': proc.pid,
                'name': proc.name(),
                'status': proc.status(),
                'username': proc.username(),
                'cpu_percent': proc.cpu_percent(interval=0.1),
                'memory_percent': proc.memory_percent(),
                'memory_mb': proc.memory_info().rss / (1024 * 1024),
                'num_threads': proc.num_threads(),
                'create_time': proc.create_time(),
                'cmdline': ' '.join(proc.cmdline()) if proc.cmdline() else 'N/A',
                'cwd': proc.cwd() if hasattr(proc, 'cwd') else 'N/A',
                'nice': proc.nice(),
                'num_fds': proc.num_fds() if hasattr(proc, 'num_fds') else 'N/A'
            }
            
            return info
        
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            return None
    
    def kill_process(self, pid: int, force=False) -> tuple[bool, str]:
        """Kill a process"""
        try:
            proc = psutil.Process(pid)
            name = proc.name()
            
            if force:
                proc.kill()  # SIGKILL
                return True, f"Process {name} (PID {pid}) forcefully killed"
            else:
                proc.terminate()  # SIGTERM
                return True, f"Process {name} (PID {pid}) terminated"
        
        except psutil.NoSuchProcess:
            return False, f"Process {pid} not found"
        except psutil.AccessDenied:
            return False, f"Access denied. Need root privileges to kill PID {pid}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def change_priority(self, pid: int, nice_value: int) -> tuple[bool, str]:
        """Change process priority (nice value)"""
        try:
            proc = psutil.Process(pid)
            name = proc.name()
            old_nice = proc.nice()
            
            proc.nice(nice_value)
            
            return True, f"Priority changed for {name} (PID {pid})\nOld nice: {old_nice} → New nice: {nice_value}"
        
        except psutil.NoSuchProcess:
            return False, f"Process {pid} not found"
        except psutil.AccessDenied:
            return False, f"Access denied. Need root privileges to change priority of PID {pid}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def suspend_process(self, pid: int) -> tuple[bool, str]:
        """Suspend a process"""
        try:
            proc = psutil.Process(pid)
            name = proc.name()
            proc.suspend()
            return True, f"Process {name} (PID {pid}) suspended"
        except psutil.NoSuchProcess:
            return False, f"Process {pid} not found"
        except psutil.AccessDenied:
            return False, f"Access denied"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def resume_process(self, pid: int) -> tuple[bool, str]:
        """Resume a suspended process"""
        try:
            proc = psutil.Process(pid)
            name = proc.name()
            proc.resume()
            return True, f"Process {name} (PID {pid}) resumed"
        except psutil.NoSuchProcess:
            return False, f"Process {pid} not found"
        except psutil.AccessDenied:
            return False, f"Access denied"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_users(self) -> List[str]:
        """Get list of unique usernames"""
        try:
            users = set()
            for proc in psutil.process_iter(['username']):
                try:
                    username = proc.info.get('username')
                    if username:
                        users.add(username)
                except:
                    continue
            return sorted(list(users))
        except Exception as e:
            return []
    
    def format_process_list(self, processes: List[Dict], title: str = "PROCESSES") -> str:
        """Format process list for Telegram"""
        if not processes:
            return f"*{title}*\n\n📭 No processes found"
        
        text = f"*{title}*\n"
        text += f"_Showing {len(processes)} processes_\n\n"
        
        for proc in processes[:15]:  # Limit to 15 for readability
            pid = proc.get('pid', 0)
            name = proc.get('name', 'N/A')
            cpu = proc.get('cpu_percent', 0)
            mem = proc.get('memory_percent', 0)
            status = proc.get('status', 'N/A')
            
            # Status icon
            status_icon = "🟢" if status == "running" else "🟡" if status == "sleeping" else "⚪"
            
            text += f"{status_icon} *{name}* `[{pid}]`\n"
            text += f"  CPU: {cpu:.1f}% | MEM: {mem:.1f}%\n"
            text += f"  Status: {status}\n\n"
        
        if len(processes) > 15:
            text += f"_...and {len(processes) - 15} more processes_\n"
        
        return text
    
    def format_process_detail(self, info: Dict) -> str:
        """Format detailed process info for Telegram"""
        from datetime import datetime
        
        text = f"*📊 PROCESS DETAILS*\n\n"
        text += f"*Name:* `{info['name']}`\n"
        text += f"*PID:* `{info['pid']}`\n"
        text += f"*Status:* {info['status']}\n"
        text += f"*User:* {info['username']}\n\n"
        
        text += f"*Performance:*\n"
        text += f"  CPU: {info['cpu_percent']:.1f}%\n"
        text += f"  Memory: {info['memory_percent']:.1f}% ({info['memory_mb']:.1f} MB)\n"
        text += f"  Threads: {info['num_threads']}\n"
        text += f"  Priority (nice): {info['nice']}\n\n"
        
        if info.get('num_fds') != 'N/A':
            text += f"*File Descriptors:* {info['num_fds']}\n"
        
        text += f"\n*Created:* {datetime.fromtimestamp(info['create_time']).strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        if info.get('cwd') != 'N/A':
            text += f"*Working Dir:* `{info['cwd']}`\n"
        
        # Truncate cmdline if too long
        cmdline = info.get('cmdline', 'N/A')
        if len(cmdline) > 100:
            cmdline = cmdline[:100] + '...'
        text += f"\n*Command:* `{cmdline}`\n"
        
        return text
