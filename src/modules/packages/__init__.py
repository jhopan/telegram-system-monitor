"""
Package Management Module

This module provides APT package management functionality.
Requires apt/dpkg to be installed on the system.
"""

from .manager import PackageManager

__all__ = ['PackageManager']
