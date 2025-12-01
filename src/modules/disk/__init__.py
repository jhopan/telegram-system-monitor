"""
Disk Module - __init__.py
"""
from .info import get_disk_info
from .partitions import get_partitions_info
from .io_stats import get_disk_io_stats

__all__ = [
    'get_disk_info',
    'get_partitions_info',
    'get_disk_io_stats',
]
