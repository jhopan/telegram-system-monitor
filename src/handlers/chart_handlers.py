"""
Chart Handlers
Handle chart generation commands
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from src.utils.decorators import require_admin
from src.modules.charts import (
    generate_cpu_chart, generate_memory_chart,
    generate_disk_chart, generate_network_chart
)


@require_admin
async def chart_cpu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate CPU usage chart"""
    await update.message.reply_text("📊 Generating CPU chart... (this may take a moment)")
    
    try:
        # Generate chart
        chart = generate_cpu_chart(duration_minutes=60)
        
        # Send chart
        await update.message.reply_photo(
            photo=chart,
            caption="📊 *CPU Usage Chart - Last 60 Minutes*",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error generating chart: {str(e)}")


@require_admin
async def chart_memory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate memory usage chart"""
    await update.message.reply_text("📊 Generating memory chart...")
    
    try:
        # Generate chart
        chart = generate_memory_chart()
        
        # Send chart
        await update.message.reply_photo(
            photo=chart,
            caption="🧠 *Memory Usage Chart*",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error generating chart: {str(e)}")


@require_admin
async def chart_disk_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate disk usage chart"""
    await update.message.reply_text("📊 Generating disk chart...")
    
    try:
        # Generate chart
        chart = generate_disk_chart()
        
        # Send chart
        await update.message.reply_photo(
            photo=chart,
            caption="💾 *Disk Usage Chart*",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error generating chart: {str(e)}")


@require_admin
async def chart_network_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate network traffic chart"""
    await update.message.reply_text("📊 Generating network chart... (monitoring for 60 seconds)")
    
    try:
        # Generate chart (will take 60 seconds)
        chart = generate_network_chart(duration_seconds=60)
        
        # Send chart
        await update.message.reply_photo(
            photo=chart,
            caption="🌐 *Network Traffic Chart - 60 Seconds*",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error generating chart: {str(e)}")


@require_admin
async def charts_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show charts menu"""
    text = """
📊 *CHARTS & VISUALIZATION*

Generate visual charts untuk monitoring:
"""
    keyboard = [
        [
            InlineKeyboardButton("🔥 CPU Chart", callback_data='chart_cpu'),
            InlineKeyboardButton("🧠 Memory Chart", callback_data='chart_memory')
        ],
        [
            InlineKeyboardButton("💾 Disk Chart", callback_data='chart_disk'),
            InlineKeyboardButton("🌐 Network Chart", callback_data='chart_network')
        ],
        [InlineKeyboardButton("◀️ Back to Tools", callback_data='menu_tools')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def handle_chart_callback(query, chart_type):
    """Handle chart generation from callback"""
    try:
        await query.edit_message_text(f"📊 Generating {chart_type} chart... Please wait.")
        
        # Generate chart based on type
        if chart_type == 'cpu':
            chart = generate_cpu_chart(duration_minutes=60)
            caption = "📊 *CPU Usage Chart - Last 60 Minutes*"
        elif chart_type == 'memory':
            chart = generate_memory_chart()
            caption = "🧠 *Memory Usage Chart*"
        elif chart_type == 'disk':
            chart = generate_disk_chart()
            caption = "💾 *Disk Usage Chart*"
        elif chart_type == 'network':
            await query.edit_message_text("📊 Generating network chart... (monitoring for 60 seconds)")
            chart = generate_network_chart(duration_seconds=60)
            caption = "🌐 *Network Traffic Chart - 60 Seconds*"
        else:
            await query.edit_message_text("❌ Unknown chart type")
            return
        
        # Send chart
        keyboard = [
            [InlineKeyboardButton("◀️ Back to Charts", callback_data='menu_charts')],
            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_photo(
            photo=chart,
            caption=caption,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
        
        # Delete loading message
        await query.message.delete()
        
    except Exception as e:
        keyboard = [[InlineKeyboardButton("◀️ Back", callback_data='menu_charts')]]
        await query.edit_message_text(
            f"❌ Error generating chart: {str(e)}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
