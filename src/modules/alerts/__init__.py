"""
Alert System Module
Monitor thresholds and send notifications
"""
from .manager import AlertManager
from .thresholds import AlertThresholds
from .checker import AlertChecker

# Global alert manager instance
alert_manager = AlertManager()
