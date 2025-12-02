"""
Docker Module

This module provides Docker monitoring and management functionality.
Requires Docker to be installed and running on the system.
"""

from .manager import DockerManager

__all__ = ['DockerManager']
