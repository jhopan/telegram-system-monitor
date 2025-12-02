"""
Report Handlers
Manage scheduled reports via inline keyboard
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from src.utils.decorators import require_admin
from src.modules.reports import ReportGenerator
import json
from pathlib import Path


@require_admin
async def reports_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show reports main menu"""
    text = """
📝 *SCHEDULED REPORTS*

Generate and schedule system reports
"""
    keyboard = [
        [
            InlineKeyboardButton("📊 Generate Daily", callback_data='report_generate_daily'),
            InlineKeyboardButton("📈 Generate Weekly", callback_data='report_generate_weekly')
        ],
        [
            InlineKeyboardButton("⚙️ Schedule Settings", callback_data='report_settings'),
            InlineKeyboardButton("📜 Report History", callback_data='report_history')
        ],
        [InlineKeyboardButton("◀️ Back to Tools", callback_data='menu_tools')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def show_reports_menu(query):
    """Show reports menu"""
    text = """
📝 *SCHEDULED REPORTS*

Generate and schedule system reports
"""
    keyboard = [
        [
            InlineKeyboardButton("📊 Generate Daily", callback_data='report_generate_daily'),
            InlineKeyboardButton("📈 Generate Weekly", callback_data='report_generate_weekly')
        ],
        [
            InlineKeyboardButton("⚙️ Schedule Settings", callback_data='report_settings'),
            InlineKeyboardButton("📜 Report History", callback_data='report_history')
        ],
        [InlineKeyboardButton("◀️ Back to Tools", callback_data='menu_tools')],
        [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def generate_daily_report(query):
    """Generate and send daily report"""
    await query.edit_message_text("⏳ Generating daily report...")
    
    try:
        generator = ReportGenerator()
        report = generator.generate_daily_report()
        text = generator.format_daily_report(report)
        
        keyboard = [
            [InlineKeyboardButton("◀️ Back", callback_data='menu_reports')],
            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    except Exception as e:
        await query.edit_message_text(
            f"❌ Error generating report: {str(e)}",
            parse_mode=ParseMode.MARKDOWN
        )


async def generate_weekly_report(query):
    """Generate and send weekly report"""
    await query.edit_message_text("⏳ Generating weekly report...")
    
    try:
        generator = ReportGenerator()
        report = generator.generate_weekly_report()
        text = generator.format_weekly_report(report)
        
        keyboard = [
            [InlineKeyboardButton("◀️ Back", callback_data='menu_reports')],
            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    except Exception as e:
        await query.edit_message_text(
            f"❌ Error generating report: {str(e)}",
            parse_mode=ParseMode.MARKDOWN
        )


async def show_report_settings(query):
    """Show report schedule settings"""
    # Load settings
    settings_file = Path('config/report_settings.json')
    if settings_file.exists():
        with open(settings_file, 'r') as f:
            settings = json.load(f)
    else:
        settings = {
            'daily_enabled': False,
            'daily_time': '09:00',
            'weekly_enabled': False,
            'weekly_day': 'monday',
            'weekly_time': '09:00'
        }
    
    daily_status = "✅ Enabled" if settings.get('daily_enabled') else "❌ Disabled"
    weekly_status = "✅ Enabled" if settings.get('weekly_enabled') else "❌ Disabled"
    
    text = f"""
⚙️ *REPORT SCHEDULE SETTINGS*

*Daily Report:*
Status: {daily_status}
Time: {settings.get('daily_time', '09:00')}

*Weekly Report:*
Status: {weekly_status}
Day: {settings.get('weekly_day', 'monday').title()}
Time: {settings.get('weekly_time', '09:00')}

_Scheduled reports will be sent automatically_
"""
    
    keyboard = [
        [
            InlineKeyboardButton("📊 Daily Settings", callback_data='report_set_daily'),
            InlineKeyboardButton("📈 Weekly Settings", callback_data='report_set_weekly')
        ],
        [InlineKeyboardButton("◀️ Back", callback_data='menu_reports')],
        [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def show_daily_settings(query):
    """Show daily report settings"""
    settings_file = Path('config/report_settings.json')
    if settings_file.exists():
        with open(settings_file, 'r') as f:
            settings = json.load(f)
    else:
        settings = {'daily_enabled': False, 'daily_time': '09:00'}
    
    status = "✅ Enabled" if settings.get('daily_enabled') else "❌ Disabled"
    
    text = f"""
📊 *DAILY REPORT SETTINGS*

Status: {status}
Current Time: {settings.get('daily_time', '09:00')}

Configure daily report schedule:
"""
    
    keyboard = []
    
    # Toggle enable/disable
    if settings.get('daily_enabled'):
        keyboard.append([InlineKeyboardButton("❌ Disable", callback_data='report_daily_disable')])
    else:
        keyboard.append([InlineKeyboardButton("✅ Enable", callback_data='report_daily_enable')])
    
    # Time presets
    keyboard.append([
        InlineKeyboardButton("06:00", callback_data='report_daily_time_06'),
        InlineKeyboardButton("09:00", callback_data='report_daily_time_09'),
        InlineKeyboardButton("12:00", callback_data='report_daily_time_12'),
        InlineKeyboardButton("18:00", callback_data='report_daily_time_18')
    ])
    
    keyboard.append([InlineKeyboardButton("◀️ Back", callback_data='report_settings')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def show_weekly_settings(query):
    """Show weekly report settings"""
    settings_file = Path('config/report_settings.json')
    if settings_file.exists():
        with open(settings_file, 'r') as f:
            settings = json.load(f)
    else:
        settings = {'weekly_enabled': False, 'weekly_day': 'monday', 'weekly_time': '09:00'}
    
    status = "✅ Enabled" if settings.get('weekly_enabled') else "❌ Disabled"
    
    text = f"""
📈 *WEEKLY REPORT SETTINGS*

Status: {status}
Day: {settings.get('weekly_day', 'monday').title()}
Time: {settings.get('weekly_time', '09:00')}

Configure weekly report schedule:
"""
    
    keyboard = []
    
    # Toggle enable/disable
    if settings.get('weekly_enabled'):
        keyboard.append([InlineKeyboardButton("❌ Disable", callback_data='report_weekly_disable')])
    else:
        keyboard.append([InlineKeyboardButton("✅ Enable", callback_data='report_weekly_enable')])
    
    # Day selection
    keyboard.append([
        InlineKeyboardButton("Mon", callback_data='report_weekly_day_monday'),
        InlineKeyboardButton("Tue", callback_data='report_weekly_day_tuesday'),
        InlineKeyboardButton("Wed", callback_data='report_weekly_day_wednesday')
    ])
    keyboard.append([
        InlineKeyboardButton("Thu", callback_data='report_weekly_day_thursday'),
        InlineKeyboardButton("Fri", callback_data='report_weekly_day_friday'),
        InlineKeyboardButton("Sat", callback_data='report_weekly_day_saturday'),
        InlineKeyboardButton("Sun", callback_data='report_weekly_day_sunday')
    ])
    
    # Time presets
    keyboard.append([
        InlineKeyboardButton("06:00", callback_data='report_weekly_time_06'),
        InlineKeyboardButton("09:00", callback_data='report_weekly_time_09'),
        InlineKeyboardButton("12:00", callback_data='report_weekly_time_12')
    ])
    
    keyboard.append([InlineKeyboardButton("◀️ Back", callback_data='report_settings')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def show_report_history(query):
    """Show report history"""
    report_dir = Path('logs/reports')
    
    if not report_dir.exists():
        text = "*📜 REPORT HISTORY*\n\n📭 No reports generated yet"
    else:
        reports = sorted(report_dir.glob('*.json'), reverse=True)[:10]
        
        if not reports:
            text = "*📜 REPORT HISTORY*\n\n📭 No reports found"
        else:
            text = "*📜 REPORT HISTORY*\n\n"
            text += f"_Last {len(reports)} reports:_\n\n"
            
            for report_file in reports:
                try:
                    with open(report_file, 'r') as f:
                        report = json.load(f)
                    
                    report_type = report.get('type', 'unknown')
                    timestamp = report.get('timestamp', 'N/A')[:19]
                    
                    icon = "📊" if report_type == 'daily' else "📈"
                    text += f"{icon} {report_type.title()} - {timestamp}\n"
                except:
                    continue
    
    keyboard = [
        [InlineKeyboardButton("🗑️ Clear History", callback_data='report_clear_history')],
        [InlineKeyboardButton("◀️ Back", callback_data='menu_reports')],
        [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def handle_report_action(query, action, value=None):
    """Handle report configuration actions"""
    try:
        settings_file = Path('config/report_settings.json')
        
        # Load current settings
        if settings_file.exists():
            with open(settings_file, 'r') as f:
                settings = json.load(f)
        else:
            settings = {
                'daily_enabled': False,
                'daily_time': '09:00',
                'weekly_enabled': False,
                'weekly_day': 'monday',
                'weekly_time': '09:00'
            }
        
        # Update settings
        if action == 'daily_enable':
            settings['daily_enabled'] = True
            await query.answer("✅ Daily reports enabled")
        elif action == 'daily_disable':
            settings['daily_enabled'] = False
            await query.answer("❌ Daily reports disabled")
        elif action == 'daily_time':
            settings['daily_time'] = f"{value:02d}:00"
            await query.answer(f"✅ Time set to {value:02d}:00")
        elif action == 'weekly_enable':
            settings['weekly_enabled'] = True
            await query.answer("✅ Weekly reports enabled")
        elif action == 'weekly_disable':
            settings['weekly_enabled'] = False
            await query.answer("❌ Weekly reports disabled")
        elif action == 'weekly_day':
            settings['weekly_day'] = value
            await query.answer(f"✅ Day set to {value.title()}")
        elif action == 'weekly_time':
            settings['weekly_time'] = f"{value:02d}:00"
            await query.answer(f"✅ Time set to {value:02d}:00")
        elif action == 'clear_history':
            report_dir = Path('logs/reports')
            if report_dir.exists():
                for f in report_dir.glob('*.json'):
                    f.unlink()
            await query.answer("✅ History cleared")
            await show_report_history(query)
            return
        
        # Save settings
        settings_file.parent.mkdir(parents=True, exist_ok=True)
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
        
        # Show updated menu
        if action.startswith('daily'):
            await show_daily_settings(query)
        elif action.startswith('weekly'):
            await show_weekly_settings(query)
    
    except Exception as e:
        await query.answer(f"❌ Error: {str(e)}")
