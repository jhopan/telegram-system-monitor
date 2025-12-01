"""
Service Manager Module
Manajemen systemd services
"""
import subprocess
from typing import Optional


def list_services(filter_status: Optional[str] = None) -> str:
    """
    List semua service systemd
    
    Args:
        filter_status: None (all), 'running', 'failed', 'inactive'
    """
    info = f"⚙️ *SYSTEMD SERVICES*\n\n"
    
    try:
        cmd = ['systemctl', 'list-units', '--type=service', '--all', '--no-pager']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            services = []
            
            for line in lines:
                # Parse service line
                if '.service' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        name = parts[0]
                        load = parts[1]
                        active = parts[2]
                        sub = parts[3]
                        
                        # Filter by status if requested
                        if filter_status:
                            if filter_status == 'running' and active != 'active':
                                continue
                            elif filter_status == 'failed' and active != 'failed':
                                continue
                            elif filter_status == 'inactive' and active == 'active':
                                continue
                        
                        services.append({
                            'name': name,
                            'active': active,
                            'sub': sub
                        })
            
            # Group by status
            running = [s for s in services if s['active'] == 'active']
            failed = [s for s in services if s['active'] == 'failed']
            inactive = [s for s in services if s['active'] not in ['active', 'failed']]
            
            info += f"*Total Services:* {len(services)}\n"
            info += f"*Running:* {len(running)}\n"
            info += f"*Failed:* {len(failed)}\n"
            info += f"*Inactive:* {len(inactive)}\n\n"
            
            if filter_status == 'running':
                info += "*RUNNING SERVICES (max 20):*\n\n"
                for svc in running[:20]:
                    info += f"✅ `{svc['name']}`\n"
            elif filter_status == 'failed':
                info += "*FAILED SERVICES:*\n\n"
                if failed:
                    for svc in failed:
                        info += f"❌ `{svc['name']}`\n"
                else:
                    info += "Tidak ada service yang failed\n"
            elif filter_status == 'inactive':
                info += "*INACTIVE SERVICES (max 20):*\n\n"
                for svc in inactive[:20]:
                    info += f"⭕ `{svc['name']}`\n"
            else:
                # Show summary
                if failed:
                    info += "*FAILED SERVICES:*\n"
                    for svc in failed[:10]:
                        info += f"❌ `{svc['name']}`\n"
                    info += "\n"
                
                info += f"*RUNNING SERVICES (showing {min(15, len(running))}/{len(running)}):*\n"
                for svc in running[:15]:
                    info += f"✅ `{svc['name']}`\n"
        else:
            info += f"❌ Error: {result.stderr}\n"
            
    except Exception as e:
        info += f"❌ Error: {str(e)}\n"
    
    return info


def get_service_status(service_name: str) -> str:
    """Cek status detail sebuah service"""
    # Clean service name
    if not service_name.endswith('.service'):
        service_name += '.service'
    
    info = f"🔍 *STATUS: {service_name}*\n\n"
    
    try:
        result = subprocess.run(
            ['systemctl', 'status', service_name, '--no-pager'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Format output
        output = result.stdout
        
        # Extract important info
        lines = output.split('\n')
        formatted_lines = []
        
        for line in lines[:20]:  # Limit to first 20 lines
            if line.strip():
                formatted_lines.append(line)
        
        info += f"```\n" + '\n'.join(formatted_lines) + "\n```\n"
        
    except Exception as e:
        info += f"❌ Error: {str(e)}\n"
    
    return info


def start_service(service_name: str) -> str:
    """Start sebuah service"""
    if not service_name.endswith('.service'):
        service_name += '.service'
    
    info = f"▶️ *STARTING: {service_name}*\n\n"
    
    try:
        result = subprocess.run(
            ['sudo', 'systemctl', 'start', service_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            info += f"✅ Service {service_name} berhasil di-start\n"
            
            # Check status
            status_result = subprocess.run(
                ['systemctl', 'is-active', service_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            info += f"*Status:* {status_result.stdout.strip()}\n"
        else:
            info += f"❌ Gagal start service\n"
            info += f"Error: {result.stderr}\n"
            
    except Exception as e:
        info += f"❌ Error: {str(e)}\n"
    
    return info


def stop_service(service_name: str) -> str:
    """Stop sebuah service"""
    if not service_name.endswith('.service'):
        service_name += '.service'
    
    info = f"⏹️ *STOPPING: {service_name}*\n\n"
    
    try:
        result = subprocess.run(
            ['sudo', 'systemctl', 'stop', service_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            info += f"✅ Service {service_name} berhasil di-stop\n"
            
            # Check status
            status_result = subprocess.run(
                ['systemctl', 'is-active', service_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            info += f"*Status:* {status_result.stdout.strip()}\n"
        else:
            info += f"❌ Gagal stop service\n"
            info += f"Error: {result.stderr}\n"
            
    except Exception as e:
        info += f"❌ Error: {str(e)}\n"
    
    return info


def restart_service(service_name: str) -> str:
    """Restart sebuah service"""
    if not service_name.endswith('.service'):
        service_name += '.service'
    
    info = f"🔄 *RESTARTING: {service_name}*\n\n"
    
    try:
        result = subprocess.run(
            ['sudo', 'systemctl', 'restart', service_name],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0:
            info += f"✅ Service {service_name} berhasil di-restart\n"
            
            # Check status
            status_result = subprocess.run(
                ['systemctl', 'is-active', service_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            info += f"*Status:* {status_result.stdout.strip()}\n"
        else:
            info += f"❌ Gagal restart service\n"
            info += f"Error: {result.stderr}\n"
            
    except Exception as e:
        info += f"❌ Error: {str(e)}\n"
    
    return info


def enable_service(service_name: str) -> str:
    """Enable service (auto-start on boot)"""
    if not service_name.endswith('.service'):
        service_name += '.service'
    
    info = f"🔓 *ENABLING: {service_name}*\n\n"
    
    try:
        result = subprocess.run(
            ['sudo', 'systemctl', 'enable', service_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            info += f"✅ Service {service_name} berhasil di-enable\n"
            info += "Service akan auto-start saat boot\n"
        else:
            info += f"❌ Gagal enable service\n"
            info += f"Error: {result.stderr}\n"
            
    except Exception as e:
        info += f"❌ Error: {str(e)}\n"
    
    return info


def disable_service(service_name: str) -> str:
    """Disable service (no auto-start on boot)"""
    if not service_name.endswith('.service'):
        service_name += '.service'
    
    info = f"🔒 *DISABLING: {service_name}*\n\n"
    
    try:
        result = subprocess.run(
            ['sudo', 'systemctl', 'disable', service_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            info += f"✅ Service {service_name} berhasil di-disable\n"
            info += "Service tidak akan auto-start saat boot\n"
        else:
            info += f"❌ Gagal disable service\n"
            info += f"Error: {result.stderr}\n"
            
    except Exception as e:
        info += f"❌ Error: {str(e)}\n"
    
    return info


def get_service_logs(service_name: str, lines: int = 50) -> str:
    """Dapatkan log service dari journalctl"""
    if not service_name.endswith('.service'):
        service_name += '.service'
    
    info = f"📋 *LOGS: {service_name}*\n\n"
    
    try:
        result = subprocess.run(
            ['journalctl', '-u', service_name, '-n', str(lines), '--no-pager'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            logs = result.stdout
            # Truncate if too long
            if len(logs) > 3500:
                logs = logs[-3500:]
                info += "... (output dipotong)\n\n"
            
            info += f"```\n{logs}\n```\n"
        else:
            info += f"❌ Tidak dapat membaca logs\n"
            info += f"Error: {result.stderr}\n"
            
    except Exception as e:
        info += f"❌ Error: {str(e)}\n"
    
    return info
