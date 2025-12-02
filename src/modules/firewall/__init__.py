"""
Firewall Module

This module provides UFW (Uncomplicated Firewall) management functionality.
Requires UFW to be installed on the system.
"""

from .manager import FirewallManager

__all__ = ['FirewallManager']
