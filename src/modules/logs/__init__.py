"""
Logs Module

This module provides system logs viewing functionality.
Supports systemd journal, syslog, and application logs.
"""

from .manager import LogsManager

__all__ = ['LogsManager']
