"""
Chart Generator Module
Generate visualization charts using matplotlib
"""
import matplotlib
matplotlib.use('Agg')  # Non-GUI backend
import matplotlib.pyplot as plt
import psutil
import time
from datetime import datetime, timedelta
from io import BytesIO


def generate_cpu_chart(duration_minutes=60):
    """
    Generate CPU usage chart
    
    Args:
        duration_minutes: Duration to collect data (default: 60 minutes)
    
    Returns:
        BytesIO: Image buffer
    """
    # Collect CPU data
    timestamps = []
    cpu_percent = []
    
    # Get historical data (simulate with current for now)
    # In production, you'd store this in database
    interval = 5  # seconds
    points = min(duration_minutes * 12, 60)  # Max 60 points
    
    for i in range(points):
        timestamps.append(datetime.now() - timedelta(minutes=duration_minutes - (i * duration_minutes/points)))
        cpu_percent.append(psutil.cpu_percent(interval=0.1))
    
    # Create chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(timestamps, cpu_percent, linewidth=2, color='#2196F3', marker='o', markersize=4)
    ax.fill_between(timestamps, cpu_percent, alpha=0.3, color='#2196F3')
    
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('CPU Usage (%)', fontsize=12)
    ax.set_title(f'CPU Usage - Last {duration_minutes} Minutes', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 100)
    
    # Format x-axis
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save to buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return buf


def generate_memory_chart():
    """
    Generate memory usage chart (RAM + SWAP)
    
    Returns:
        BytesIO: Image buffer
    """
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    # Data for pie chart
    labels = ['Used RAM', 'Free RAM', 'Used SWAP', 'Free SWAP']
    sizes = [
        memory.used / (1024**3),
        memory.available / (1024**3),
        swap.used / (1024**3) if swap.total > 0 else 0,
        (swap.total - swap.used) / (1024**3) if swap.total > 0 else 0
    ]
    colors = ['#FF5252', '#4CAF50', '#FF9800', '#8BC34A']
    explode = (0.1, 0, 0.1, 0) if swap.total > 0 else (0.1, 0, 0, 0)
    
    # Create chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Pie chart
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    ax1.set_title('Memory Distribution', fontsize=14, fontweight='bold')
    
    # Bar chart
    categories = ['RAM', 'SWAP']
    used = [memory.percent, swap.percent if swap.total > 0 else 0]
    
    bars = ax2.bar(categories, used, color=['#2196F3', '#FF9800'], width=0.6)
    ax2.set_ylabel('Usage (%)', fontsize=12)
    ax2.set_title('Memory Usage Percentage', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    # Save to buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return buf


def generate_disk_chart():
    """
    Generate disk usage chart for all partitions
    
    Returns:
        BytesIO: Image buffer
    """
    partitions = psutil.disk_partitions()
    
    devices = []
    usage_percent = []
    colors_list = []
    
    for partition in partitions:
        if partition.fstype:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                devices.append(partition.device.split('/')[-1][:10])
                usage_percent.append(usage.percent)
                
                # Color based on usage
                if usage.percent >= 90:
                    colors_list.append('#F44336')  # Red
                elif usage.percent >= 70:
                    colors_list.append('#FF9800')  # Orange
                else:
                    colors_list.append('#4CAF50')  # Green
            except:
                continue
    
    if not devices:
        devices = ['No Data']
        usage_percent = [0]
        colors_list = ['#CCCCCC']
    
    # Create chart
    fig, ax = plt.subplots(figsize=(12, max(6, len(devices) * 0.5)))
    
    bars = ax.barh(devices, usage_percent, color=colors_list)
    ax.set_xlabel('Usage (%)', fontsize=12)
    ax.set_title('Disk Usage by Partition', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 100)
    ax.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for i, (bar, percent) in enumerate(zip(bars, usage_percent)):
        width = bar.get_width()
        ax.text(width + 2, bar.get_y() + bar.get_height()/2.,
                f'{percent:.1f}%', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    
    # Save to buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return buf


def generate_network_chart(duration_seconds=60):
    """
    Generate network traffic chart
    
    Args:
        duration_seconds: Duration to monitor (default: 60 seconds)
    
    Returns:
        BytesIO: Image buffer
    """
    # Collect network data
    timestamps = []
    bytes_sent_list = []
    bytes_recv_list = []
    
    initial = psutil.net_io_counters()
    last_sent = initial.bytes_sent
    last_recv = initial.bytes_recv
    
    points = min(duration_seconds, 30)  # Max 30 points
    interval = duration_seconds / points
    
    for i in range(points):
        time.sleep(interval)
        current = psutil.net_io_counters()
        
        sent_rate = (current.bytes_sent - last_sent) / interval / 1024  # KB/s
        recv_rate = (current.bytes_recv - last_recv) / interval / 1024  # KB/s
        
        timestamps.append(i * interval)
        bytes_sent_list.append(sent_rate)
        bytes_recv_list.append(recv_rate)
        
        last_sent = current.bytes_sent
        last_recv = current.bytes_recv
    
    # Create chart
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(timestamps, bytes_sent_list, linewidth=2, color='#FF5722', 
            marker='o', markersize=4, label='Upload')
    ax.plot(timestamps, bytes_recv_list, linewidth=2, color='#2196F3', 
            marker='s', markersize=4, label='Download')
    
    ax.fill_between(timestamps, bytes_sent_list, alpha=0.3, color='#FF5722')
    ax.fill_between(timestamps, bytes_recv_list, alpha=0.3, color='#2196F3')
    
    ax.set_xlabel('Time (seconds)', fontsize=12)
    ax.set_ylabel('Speed (KB/s)', fontsize=12)
    ax.set_title(f'Network Traffic - {duration_seconds} Seconds', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save to buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return buf
