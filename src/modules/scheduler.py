"""
Background Scheduler
For periodic tasks (alerts, reports, etc)
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import logging
import json
from pathlib import Path
from src.modules.alerts import alert_manager
from src.modules.alerts.thresholds import AlertThresholds
from src.modules.alerts.checker import AlertChecker
from src.modules.reports import ReportGenerator

logger = logging.getLogger(__name__)


class BackgroundScheduler:
    """Handle background tasks"""
    
    def __init__(self, bot_application):
        self.bot = bot_application.bot
        self.scheduler = AsyncIOScheduler()
        self.thresholds = AlertThresholds()
        self.checker = AlertChecker(self.thresholds, alert_manager)
        self.report_generator = ReportGenerator()
        self.notified_alerts = set()  # Track notified alerts to avoid spam
    
    async def check_alerts_task(self):
        """Periodic alert checking task"""
        try:
            alerts = self.checker.check_all()
            
            # Send notifications for new alerts
            for alert in alerts:
                alert_key = f"{alert['metric']}_{alert['value']:.0f}"
                
                # Only notify if this is a new alert
                if alert_key not in self.notified_alerts:
                    await self.send_alert_notification(alert)
                    self.notified_alerts.add(alert_key)
            
            # Clear notified alerts that are resolved
            active_metrics = {alert['metric'] for alert in alerts}
            self.notified_alerts = {
                key for key in self.notified_alerts
                if key.split('_')[0] in active_metrics
            }
            
        except Exception as e:
            logger.error(f"Error in alert checking task: {e}")
    
    async def daily_report_task(self):
        """Generate and send daily report"""
        try:
            logger.info("Generating daily report...")
            report = self.report_generator.generate_daily_report()
            text = self.report_generator.format_daily_report(report)
            
            from config.settings import config
            
            # Send to all admin users
            for user_id in config.ADMIN_USER_IDS:
                try:
                    await self.bot.send_message(
                        chat_id=user_id,
                        text=text,
                        parse_mode='Markdown'
                    )
                    logger.info(f"Daily report sent to {user_id}")
                except Exception as e:
                    logger.error(f"Failed to send daily report to {user_id}: {e}")
        
        except Exception as e:
            logger.error(f"Error in daily report task: {e}")
    
    async def weekly_report_task(self):
        """Generate and send weekly report"""
        try:
            logger.info("Generating weekly report...")
            report = self.report_generator.generate_weekly_report()
            text = self.report_generator.format_weekly_report(report)
            
            from config.settings import config
            
            # Send to all admin users
            for user_id in config.ADMIN_USER_IDS:
                try:
                    await self.bot.send_message(
                        chat_id=user_id,
                        text=text,
                        parse_mode='Markdown'
                    )
                    logger.info(f"Weekly report sent to {user_id}")
                except Exception as e:
                    logger.error(f"Failed to send weekly report to {user_id}: {e}")
        
        except Exception as e:
            logger.error(f"Error in weekly report task: {e}")
    
    def _load_report_settings(self):
        """Load report schedule settings"""
        settings_file = Path('config/report_settings.json')
        if settings_file.exists():
            try:
                with open(settings_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'daily_enabled': False,
            'daily_time': '09:00',
            'weekly_enabled': False,
            'weekly_day': 'monday',
            'weekly_time': '09:00'
        }
    
    def _schedule_reports(self):
        """Schedule report tasks based on settings"""
        settings = self._load_report_settings()
        
        # Daily report
        if settings.get('daily_enabled'):
            hour, minute = map(int, settings.get('daily_time', '09:00').split(':'))
            self.scheduler.add_job(
                self.daily_report_task,
                trigger=CronTrigger(hour=hour, minute=minute),
                id='daily_report',
                name='Daily System Report',
                replace_existing=True
            )
            logger.info(f"Daily report scheduled at {hour:02d}:{minute:02d}")
        
        # Weekly report
        if settings.get('weekly_enabled'):
            hour, minute = map(int, settings.get('weekly_time', '09:00').split(':'))
            day_map = {
                'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                'friday': 4, 'saturday': 5, 'sunday': 6
            }
            day_of_week = day_map.get(settings.get('weekly_day', 'monday'), 0)
            
            self.scheduler.add_job(
                self.weekly_report_task,
                trigger=CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute),
                id='weekly_report',
                name='Weekly System Report',
                replace_existing=True
            )
            logger.info(f"Weekly report scheduled on {settings.get('weekly_day')} at {hour:02d}:{minute:02d}")
    
    async def send_alert_notification(self, alert):
        """Send alert notification to admin"""
        from config.settings import config
        
        message = f"""
⚠️ *SYSTEM ALERT*

*Metric:* {alert['metric'].upper()}
*Current Value:* {alert['value']:.1f}%
*Threshold:* {alert['threshold']}%

*Message:* {alert['message']}

_Use /alerts to manage alert settings_
"""
        
        # Send to all admin users
        for user_id in config.ADMIN_USER_IDS:
            try:
                await self.bot.send_message(
                    chat_id=user_id,
                    text=message,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Failed to send alert to {user_id}: {e}")
    
    def start(self, interval_minutes=5):
        """Start background scheduler"""
        # Add alert checking task
        self.scheduler.add_job(
            self.check_alerts_task,
            trigger=IntervalTrigger(minutes=interval_minutes),
            id='check_alerts',
            name='Check System Alerts',
            replace_existing=True
        )
        
        # Schedule reports
        self._schedule_reports()
        
        self.scheduler.start()
        logger.info(f"Background scheduler started")
        logger.info(f"  - Alert check: every {interval_minutes} min")
    
    def reload_report_schedule(self):
        """Reload report schedule (called when settings change)"""
        try:
            self._schedule_reports()
            logger.info("Report schedule reloaded")
        except Exception as e:
            logger.error(f"Error reloading report schedule: {e}")
    
    def stop(self):
        """Stop background scheduler"""
        self.scheduler.shutdown()
        logger.info("Background scheduler stopped")
