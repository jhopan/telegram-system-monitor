"""
Alert Handlers
Manage alerts via inline keyboard
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from src.utils.decorators import require_admin
from src.modules.alerts import alert_manager
from src.modules.alerts.thresholds import AlertThresholds
from src.modules.alerts.checker import AlertChecker

# Initialize
thresholds = AlertThresholds()
checker = AlertChecker(thresholds, alert_manager)


@require_admin
async def alerts_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show alerts main menu"""
    text = """
🔔 *ALERT SYSTEM*

Manage system alerts and notifications
"""
    keyboard = [
        [
            InlineKeyboardButton("⚙️ Settings", callback_data='alert_settings'),
            InlineKeyboardButton("📊 Active Alerts", callback_data='alert_active')
        ],
        [
            InlineKeyboardButton("📜 History", callback_data='alert_history'),
            InlineKeyboardButton("🔍 Check Now", callback_data='alert_check')
        ],
        [InlineKeyboardButton("◀️ Back to Tools", callback_data='menu_tools')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def show_alert_settings(query):
    """Show alert settings menu"""
    text = thresholds.format_thresholds_text()
    
    keyboard = [
        [
            InlineKeyboardButton("🔥 CPU Settings", callback_data='alert_set_cpu'),
            InlineKeyboardButton("🧠 Memory Settings", callback_data='alert_set_memory')
        ],
        [
            InlineKeyboardButton("💾 Disk Settings", callback_data='alert_set_disk'),
            InlineKeyboardButton("💿 Swap Settings", callback_data='alert_set_swap')
        ],
        [InlineKeyboardButton("◀️ Back", callback_data='menu_alerts')],
        [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def show_alert_metric_settings(query, metric):
    """Show settings for specific metric"""
    config = thresholds.get_threshold(metric)
    
    status = "✅ Enabled" if config.get('enabled') else "❌ Disabled"
    threshold_val = config.get('threshold', 0)
    duration = config.get('duration', 0)
    
    text = f"""
*🔔 {metric.upper()} ALERT SETTINGS*

Status: {status}
Threshold: {threshold_val}%
Duration: {duration} min

Configure alert settings:
"""
    
    keyboard = []
    
    # Toggle enable/disable
    if config.get('enabled'):
        keyboard.append([InlineKeyboardButton("❌ Disable", callback_data=f'alert_disable_{metric}')])
    else:
        keyboard.append([InlineKeyboardButton("✅ Enable", callback_data=f'alert_enable_{metric}')])
    
    # Threshold presets
    keyboard.append([
        InlineKeyboardButton("70%", callback_data=f'alert_thresh_{metric}_70'),
        InlineKeyboardButton("80%", callback_data=f'alert_thresh_{metric}_80'),
        InlineKeyboardButton("90%", callback_data=f'alert_thresh_{metric}_90'),
        InlineKeyboardButton("95%", callback_data=f'alert_thresh_{metric}_95')
    ])
    
    # Duration presets (for CPU/Memory)
    if metric in ['cpu', 'memory', 'swap']:
        keyboard.append([
            InlineKeyboardButton("1min", callback_data=f'alert_dur_{metric}_1'),
            InlineKeyboardButton("5min", callback_data=f'alert_dur_{metric}_5'),
            InlineKeyboardButton("10min", callback_data=f'alert_dur_{metric}_10'),
            InlineKeyboardButton("30min", callback_data=f'alert_dur_{metric}_30')
        ])
    
    keyboard.append([InlineKeyboardButton("◀️ Back", callback_data='alert_settings')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def show_active_alerts(query):
    """Show active alerts"""
    text = alert_manager.format_active_alerts()
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data='alert_active')],
        [InlineKeyboardButton("◀️ Back", callback_data='menu_alerts')],
        [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def show_alert_history(query):
    """Show alert history"""
    text = alert_manager.format_history(20)
    
    keyboard = [
        [
            InlineKeyboardButton("🗑️ Clear History", callback_data='alert_clear_history'),
            InlineKeyboardButton("🔄 Refresh", callback_data='alert_history')
        ],
        [InlineKeyboardButton("◀️ Back", callback_data='menu_alerts')],
        [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def check_alerts_now(query):
    """Check all alerts immediately"""
    await query.edit_message_text("🔍 Checking all metrics...")
    
    alerts = checker.check_all()
    
    if alerts:
        text = f"*⚠️ ALERT CHECK RESULTS*\n\n"
        text += f"Found {len(alerts)} alert(s):\n\n"
        for alert in alerts:
            text += f"• {alert['metric'].upper()}: {alert['value']:.1f}% (threshold: {alert['threshold']}%)\n"
            text += f"  {alert['message']}\n\n"
    else:
        text = "*✅ ALERT CHECK RESULTS*\n\nAll metrics are within normal range!"
    
    keyboard = [
        [InlineKeyboardButton("🔄 Check Again", callback_data='alert_check')],
        [InlineKeyboardButton("◀️ Back", callback_data='menu_alerts')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def handle_alert_action(query, action, metric=None, value=None):
    """Handle alert configuration actions"""
    try:
        if action == 'enable':
            thresholds.enable_alert(metric)
            await query.answer(f"✅ {metric.upper()} alert enabled")
            await show_alert_metric_settings(query, metric)
        
        elif action == 'disable':
            thresholds.disable_alert(metric)
            await query.answer(f"❌ {metric.upper()} alert disabled")
            await show_alert_metric_settings(query, metric)
        
        elif action == 'threshold':
            thresholds.set_threshold(metric, int(value))
            await query.answer(f"✅ Threshold set to {value}%")
            await show_alert_metric_settings(query, metric)
        
        elif action == 'duration':
            config = thresholds.get_threshold(metric)
            thresholds.set_threshold(
                metric,
                config.get('threshold', 90),
                config.get('enabled', True),
                int(value)
            )
            await query.answer(f"✅ Duration set to {value} min")
            await show_alert_metric_settings(query, metric)
        
        elif action == 'clear_history':
            alert_manager.clear_history()
            await query.answer("✅ History cleared")
            await show_alert_history(query)
    
    except Exception as e:
        await query.answer(f"❌ Error: {str(e)}")
