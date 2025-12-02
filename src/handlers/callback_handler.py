"""
Callback Query Handler
Untuk inline keyboard buttons dengan navigasi lengkap
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from src.utils.decorators import require_admin_callback
from src.modules.system import (
    get_system_info, get_cpu_info, get_memory_info, 
    get_uptime, get_processes_info, get_users_info
)
from src.modules.network import (
    get_network_info, get_network_stats, get_public_ip,
    get_connections, get_routing_table, get_dns_info
)
from src.modules.disk import get_disk_info, get_partitions_info, get_disk_io_stats
from src.modules.service import list_services
from src.modules.device import get_device_info, get_sensors_info, get_battery_info
from src.handlers.chart_handlers import handle_chart_callback
from src.handlers.alert_handlers import (
    show_alert_settings, show_alert_metric_settings,
    show_active_alerts, show_alert_history,
    check_alerts_now, handle_alert_action
)
from src.handlers.report_handlers import (
    show_reports_menu, generate_daily_report, generate_weekly_report,
    show_report_settings, show_daily_settings, show_weekly_settings,
    show_report_history, handle_report_action
)
from src.handlers.process_handlers import (
    show_processes_menu, show_top_processes, show_search_menu,
    show_filter_menu, show_users_filter, search_processes,
    filter_processes, show_process_detail, show_priority_menu,
    handle_process_action
)
from src.handlers.docker_handlers import (
    show_docker_menu, show_containers, show_container_detail,
    show_container_stats, show_container_logs, handle_container_action,
    handle_bulk_action
)
from src.handlers.package_handlers import (
    show_packages_menu, show_installed_packages, show_upgradeable_packages,
    show_package_categories, show_category_packages, show_package_info,
    handle_package_action, confirm_action
)
from src.handlers.firewall_handlers import (
    show_firewall_menu, show_firewall_rules, show_add_rule_menu,
    show_database_services, show_other_services, show_default_policies,
    show_policy_options, handle_firewall_action, confirm_firewall_action
)
from src.handlers.scripts_handlers import (
    show_scripts_menu, show_category_scripts, show_script_info,
    confirm_script_execution, execute_script, show_script_history,
    confirm_clear_history, clear_script_history
)
from src.handlers.logs_handlers import (
    show_logs_menu, show_log_type, show_application_logs,
    view_application_logs, view_logs, show_priority_filter,
    view_logs_by_priority
)
from src.handlers.service_manager_handlers import (
    show_service_manager_menu, show_services_list, show_service_detail,
    show_service_logs, show_service_dependencies, show_common_services,
    show_common_category, handle_service_action, confirm_service_action
)
from src.handlers.network_tools_handlers import (
    show_network_tools_menu, show_ping_menu, show_ping_category,
    execute_ping, show_traceroute_menu, show_traceroute_category,
    execute_traceroute, show_portscan_menu, show_portscan_category,
    execute_portscan, show_dns_menu, show_dns_type_hosts,
    execute_dns_lookup
)


@require_admin_callback
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk inline keyboard buttons dengan navigasi lengkap"""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    
    # Navigation handlers
    if callback_data == 'main_menu':
        await show_main_menu(query)
    elif callback_data == 'show_help':
        await show_help(query)
    elif callback_data == 'show_about':
        await show_about(query)
    elif callback_data == 'menu_system':
        await show_system_menu(query)
    elif callback_data == 'menu_disk':
        await show_disk_menu(query)
    elif callback_data == 'menu_network':
        await show_network_menu(query)
    elif callback_data == 'menu_service':
        await show_service_menu(query)
    elif callback_data == 'menu_device':
        await show_device_menu(query)
    elif callback_data == 'menu_tools':
        await show_tools_menu(query)
    elif callback_data == 'menu_charts':
        await show_charts_menu(query)
    elif callback_data == 'menu_alerts':
        from src.handlers.alert_handlers import show_alerts_menu
        await show_alerts_menu(query)
    elif callback_data == 'menu_reports':
        await show_reports_menu(query)
    elif callback_data == 'menu_processes':
        await show_processes_menu(query)
    elif callback_data == 'menu_docker':
        await show_docker_menu(update, context)
    elif callback_data == 'menu_packages':
        await show_packages_menu(update, context)
    elif callback_data == 'menu_firewall':
        await show_firewall_menu(update, context)
    elif callback_data == 'menu_scripts':
        await show_scripts_menu(update, context)
    elif callback_data == 'menu_logs':
        await show_logs_menu(update, context)
    elif callback_data == 'menu_servicemanager':
        await show_service_manager_menu(update, context)
    elif callback_data == 'menu_nettools':
        await show_network_tools_menu(update, context)
    # Docker handlers
    elif callback_data == 'docker_all':
        await show_containers(update, context, 'all')
    elif callback_data == 'docker_running':
        await show_containers(update, context, 'running')
    elif callback_data == 'docker_stopped':
        await show_containers(update, context, 'stopped')
    elif callback_data.startswith('docker_detail_'):
        container_id = callback_data.replace('docker_detail_', '')
        await show_container_detail(update, context, container_id)
    elif callback_data.startswith('docker_stats_'):
        container_id = callback_data.replace('docker_stats_', '')
        await show_container_stats(update, context, container_id)
    elif callback_data.startswith('docker_logs_'):
        container_id = callback_data.replace('docker_logs_', '')
        await show_container_logs(update, context, container_id)
    elif callback_data.startswith('docker_start_'):
        if callback_data == 'docker_start_all':
            await handle_bulk_action(update, context, 'start_all')
        else:
            container_id = callback_data.replace('docker_start_', '')
            await handle_container_action(update, context, 'start', container_id)
    elif callback_data.startswith('docker_stop_'):
        if callback_data == 'docker_stop_all':
            await handle_bulk_action(update, context, 'stop_all')
        else:
            container_id = callback_data.replace('docker_stop_', '')
            await handle_container_action(update, context, 'stop', container_id)
    elif callback_data.startswith('docker_restart_'):
        container_id = callback_data.replace('docker_restart_', '')
        await handle_container_action(update, context, 'restart', container_id)
    elif callback_data.startswith('docker_remove_'):
        if callback_data == 'docker_remove_stopped':
            await handle_bulk_action(update, context, 'remove_stopped')
        else:
            container_id = callback_data.replace('docker_remove_', '')
            await handle_container_action(update, context, 'remove', container_id)
    # Package handlers
    elif callback_data == 'pkg_installed':
        await show_installed_packages(update, context)
    elif callback_data == 'pkg_upgradeable':
        await show_upgradeable_packages(update, context)
    elif callback_data == 'pkg_categories':
        await show_package_categories(update, context)
    elif callback_data.startswith('pkg_cat_'):
        category = callback_data.replace('pkg_cat_', '')
        await show_category_packages(update, context, category)
    elif callback_data.startswith('pkg_info_'):
        parts = callback_data.replace('pkg_info_', '').split('_', 1)
        if len(parts) == 2:
            category, package = parts
            await show_package_info(update, context, category, package)
    elif callback_data == 'pkg_update':
        await handle_package_action(update, context, 'update')
    elif callback_data == 'pkg_upgrade_all_confirm':
        await confirm_action(update, context, 'upgrade_all', '')
    elif callback_data == 'pkg_upgrade_all':
        await handle_package_action(update, context, 'upgrade_all')
    elif callback_data == 'pkg_autoremove':
        await handle_package_action(update, context, 'autoremove')
    elif callback_data.startswith('pkg_install_'):
        package = callback_data.replace('pkg_install_', '')
        if package.endswith('_confirm'):
            package = package.replace('_confirm', '')
            await confirm_action(update, context, 'install', package)
        else:
            await handle_package_action(update, context, 'install', package)
    elif callback_data.startswith('pkg_remove_'):
        package = callback_data.replace('pkg_remove_', '')
        if package.endswith('_confirm'):
            package = package.replace('_confirm', '')
            await confirm_action(update, context, 'remove', package)
        else:
            await handle_package_action(update, context, 'remove', package)
    # Firewall handlers
    elif callback_data == 'fw_rules':
        await show_firewall_rules(update, context)
    elif callback_data == 'fw_add_menu':
        await show_add_rule_menu(update, context)
    elif callback_data == 'fw_add_db_menu':
        await show_database_services(update, context)
    elif callback_data == 'fw_add_other_menu':
        await show_other_services(update, context)
    elif callback_data.startswith('fw_add_'):
        service = callback_data.replace('fw_add_', '')
        await handle_firewall_action(update, context, 'add_rule', service)
    elif callback_data == 'fw_enable':
        await handle_firewall_action(update, context, 'enable')
    elif callback_data == 'fw_disable_confirm':
        await confirm_firewall_action(update, context, 'disable')
    elif callback_data == 'fw_disable':
        await handle_firewall_action(update, context, 'disable')
    elif callback_data == 'fw_reset_confirm':
        await confirm_firewall_action(update, context, 'reset')
    elif callback_data == 'fw_reset':
        await handle_firewall_action(update, context, 'reset')
    elif callback_data.startswith('fw_delete_'):
        parts = callback_data.replace('fw_delete_', '').split('_')
        rule_num = parts[0]
        if len(parts) > 1 and parts[1] == 'confirm':
            await confirm_firewall_action(update, context, 'delete_rule', rule_num)
        else:
            await handle_firewall_action(update, context, 'delete_rule', rule_num)
    elif callback_data == 'fw_policies':
        await show_default_policies(update, context)
    elif callback_data == 'fw_policy_incoming':
        await show_policy_options(update, context, 'incoming')
    elif callback_data == 'fw_policy_outgoing':
        await show_policy_options(update, context, 'outgoing')
    elif callback_data.startswith('fw_setpolicy_'):
        value = callback_data.replace('fw_setpolicy_', '')
        await handle_firewall_action(update, context, 'set_policy', value)
    # Scripts handlers
    elif callback_data.startswith('script_cat_'):
        category = callback_data.replace('script_cat_', '')
        await show_category_scripts(update, context, category)
    elif callback_data.startswith('script_info_'):
        parts = callback_data.replace('script_info_', '').split('_', 1)
        if len(parts) == 2:
            category, script_id = parts
            await show_script_info(update, context, category, script_id)
    elif callback_data.startswith('script_exec_'):
        parts = callback_data.replace('script_exec_', '').split('_')
        if len(parts) >= 2:
            category = parts[0]
            if parts[-1] == 'confirm':
                script_id = '_'.join(parts[1:-1])
                await confirm_script_execution(update, context, category, script_id)
            else:
                script_id = '_'.join(parts[1:])
                await execute_script(update, context, category, script_id)
    elif callback_data == 'script_history':
        await show_script_history(update, context)
    elif callback_data == 'script_clear_history_confirm':
        await confirm_clear_history(update, context)
    elif callback_data == 'script_clear_history':
        await clear_script_history(update, context)
    # Logs handlers
    elif callback_data == 'logs_menu':
        await show_logs_menu(update, context)
    elif callback_data.startswith('logs_type_'):
        log_type = callback_data.replace('logs_type_', '')
        await show_log_type(update, context, log_type)
    elif callback_data == 'logs_apps':
        await show_application_logs(update, context)
    elif callback_data.startswith('logs_app_'):
        app_name = callback_data.replace('logs_app_', '')
        await view_application_logs(update, context, app_name)
    elif callback_data.startswith('logs_view_'):
        parts = callback_data.replace('logs_view_', '').rsplit('_', 1)
        if len(parts) == 2:
            log_type, time_range = parts
            await view_logs(update, context, log_type, time_range)
    elif callback_data == 'logs_filter':
        await show_priority_filter(update, context)
    elif callback_data.startswith('logs_priority_'):
        priority = callback_data.replace('logs_priority_', '')
        await view_logs_by_priority(update, context, priority)
    # Service Manager handlers
    elif callback_data == 'svcmgr_menu':
        await show_service_manager_menu(update, context)
    elif callback_data.startswith('svcmgr_list_'):
        filter_type = callback_data.replace('svcmgr_list_', '')
        await show_services_list(update, context, filter_type)
    elif callback_data.startswith('svcmgr_page_'):
        parts = callback_data.replace('svcmgr_page_', '').rsplit('_', 1)
        if len(parts) == 2:
            filter_type, page = parts
            context.user_data['svcmgr_page'] = int(page)
            await show_services_list(update, context, filter_type)
    elif callback_data.startswith('svcmgr_detail_'):
        service_name = callback_data.replace('svcmgr_detail_', '')
        await show_service_detail(update, context, service_name)
    elif callback_data.startswith('svcmgr_logs_'):
        service_name = callback_data.replace('svcmgr_logs_', '')
        await show_service_logs(update, context, service_name)
    elif callback_data.startswith('svcmgr_deps_'):
        service_name = callback_data.replace('svcmgr_deps_', '')
        await show_service_dependencies(update, context, service_name)
    elif callback_data == 'svcmgr_common':
        await show_common_services(update, context)
    elif callback_data.startswith('svcmgr_cat_'):
        category = callback_data.replace('svcmgr_cat_', '')
        await show_common_category(update, context, category)
    elif callback_data.startswith('svcmgr_start_'):
        service_name = callback_data.replace('svcmgr_start_', '')
        await handle_service_action(update, context, service_name, 'start')
    elif callback_data.startswith('svcmgr_stop_'):
        service_name = callback_data.replace('svcmgr_stop_', '')
        await confirm_service_action(update, context, service_name, 'stop')
    elif callback_data.startswith('svcmgr_restart_'):
        service_name = callback_data.replace('svcmgr_restart_', '')
        await confirm_service_action(update, context, service_name, 'restart')
    elif callback_data.startswith('svcmgr_reload_'):
        service_name = callback_data.replace('svcmgr_reload_', '')
        await handle_service_action(update, context, service_name, 'reload')
    elif callback_data.startswith('svcmgr_enable_'):
        service_name = callback_data.replace('svcmgr_enable_', '')
        await handle_service_action(update, context, service_name, 'enable')
    elif callback_data.startswith('svcmgr_disable_'):
        service_name = callback_data.replace('svcmgr_disable_', '')
        await confirm_service_action(update, context, service_name, 'disable')
    elif callback_data.startswith('svcmgr_confirm_'):
        parts = callback_data.replace('svcmgr_confirm_', '').split('_', 1)
        if len(parts) == 2:
            action, service_name = parts
            await handle_service_action(update, context, service_name, action)
    # Network Tools handlers
    elif callback_data == 'nettools_menu':
        await show_network_tools_menu(update, context)
    elif callback_data == 'nettools_ping':
        await show_ping_menu(update, context)
    elif callback_data.startswith('nettools_ping_cat_'):
        category = callback_data.replace('nettools_ping_cat_', '')
        await show_ping_category(update, context, category)
    elif callback_data.startswith('nettools_ping_exec_'):
        host = callback_data.replace('nettools_ping_exec_', '')
        await execute_ping(update, context, host)
    elif callback_data == 'nettools_trace':
        await show_traceroute_menu(update, context)
    elif callback_data.startswith('nettools_trace_cat_'):
        category = callback_data.replace('nettools_trace_cat_', '')
        await show_traceroute_category(update, context, category)
    elif callback_data.startswith('nettools_trace_exec_'):
        host = callback_data.replace('nettools_trace_exec_', '')
        await execute_traceroute(update, context, host)
    elif callback_data == 'nettools_portscan':
        await show_portscan_menu(update, context)
    elif callback_data.startswith('nettools_port_cat_'):
        category = callback_data.replace('nettools_port_cat_', '')
        await show_portscan_category(update, context, category)
    elif callback_data.startswith('nettools_port_scan_'):
        parts = callback_data.replace('nettools_port_scan_', '').rsplit('_', 1)
        if len(parts) == 2:
            host, port = parts
            await execute_portscan(update, context, host, int(port))
    elif callback_data == 'nettools_dns':
        await show_dns_menu(update, context)
    elif callback_data.startswith('nettools_dns_type_'):
        record_type = callback_data.replace('nettools_dns_type_', '')
        await show_dns_type_hosts(update, context, record_type)
    elif callback_data.startswith('nettools_dns_query_'):
        parts = callback_data.replace('nettools_dns_query_', '').split('_', 1)
        if len(parts) == 2:
            record_type, domain = parts
            await execute_dns_lookup(update, context, domain, record_type)
    # Alert handlers
    elif callback_data == 'alert_settings':
        await show_alert_settings(query)
    elif callback_data == 'alert_active':
        await show_active_alerts(query)
    elif callback_data == 'alert_history':
        await show_alert_history(query)
    elif callback_data == 'alert_check':
        await check_alerts_now(query)
    elif callback_data.startswith('alert_set_'):
        metric = callback_data.replace('alert_set_', '')
        await show_alert_metric_settings(query, metric)
    elif callback_data.startswith('alert_enable_'):
        metric = callback_data.replace('alert_enable_', '')
        await handle_alert_action(query, 'enable', metric)
    elif callback_data.startswith('alert_disable_'):
        metric = callback_data.replace('alert_disable_', '')
        await handle_alert_action(query, 'disable', metric)
    elif callback_data.startswith('alert_thresh_'):
        parts = callback_data.replace('alert_thresh_', '').split('_')
        await handle_alert_action(query, 'threshold', parts[0], parts[1])
    elif callback_data.startswith('alert_dur_'):
        parts = callback_data.replace('alert_dur_', '').split('_')
        await handle_alert_action(query, 'duration', parts[0], parts[1])
    elif callback_data == 'alert_clear_history':
        await handle_alert_action(query, 'clear_history')
    # Report handlers
    elif callback_data == 'report_generate_daily':
        await generate_daily_report(query)
    elif callback_data == 'report_generate_weekly':
        await generate_weekly_report(query)
    elif callback_data == 'report_settings':
        await show_report_settings(query)
    elif callback_data == 'report_set_daily':
        await show_daily_settings(query)
    elif callback_data == 'report_set_weekly':
        await show_weekly_settings(query)
    elif callback_data == 'report_history':
        await show_report_history(query)
    elif callback_data == 'report_daily_enable':
        await handle_report_action(query, 'daily_enable')
    elif callback_data == 'report_daily_disable':
        await handle_report_action(query, 'daily_disable')
    elif callback_data.startswith('report_daily_time_'):
        hour = int(callback_data.replace('report_daily_time_', ''))
        await handle_report_action(query, 'daily_time', hour)
    elif callback_data == 'report_weekly_enable':
        await handle_report_action(query, 'weekly_enable')
    elif callback_data == 'report_weekly_disable':
        await handle_report_action(query, 'weekly_disable')
    elif callback_data.startswith('report_weekly_day_'):
        day = callback_data.replace('report_weekly_day_', '')
        await handle_report_action(query, 'weekly_day', day)
    elif callback_data.startswith('report_weekly_time_'):
        hour = int(callback_data.replace('report_weekly_time_', ''))
        await handle_report_action(query, 'weekly_time', hour)
    elif callback_data == 'report_clear_history':
        await handle_report_action(query, 'clear_history')
    # Process handlers
    elif callback_data == 'proc_top_cpu':
        await show_top_processes(query, 'cpu')
    elif callback_data == 'proc_top_memory':
        await show_top_processes(query, 'memory')
    elif callback_data == 'proc_all':
        await show_top_processes(query, 'pid')
    elif callback_data == 'proc_refresh':
        await show_processes_menu(query)
    elif callback_data == 'proc_search_menu':
        await show_search_menu(query)
    elif callback_data == 'proc_filter_menu':
        await show_filter_menu(query)
    elif callback_data == 'proc_filter_users':
        await show_users_filter(query)
    elif callback_data.startswith('proc_search_'):
        term = callback_data.replace('proc_search_', '')
        await search_processes(query, term)
    elif callback_data.startswith('proc_filter_'):
        status = callback_data.replace('proc_filter_', '')
        if status != 'users' and status != 'menu':
            await filter_processes(query, 'status', status)
    elif callback_data.startswith('proc_user_'):
        username = callback_data.replace('proc_user_', '')
        await filter_processes(query, 'user', username)
    elif callback_data.startswith('proc_detail_'):
        pid = callback_data.replace('proc_detail_', '')
        await show_process_detail(query, int(pid))
    elif callback_data.startswith('proc_priority_'):
        pid = callback_data.replace('proc_priority_', '')
        await show_priority_menu(query, int(pid))
    elif callback_data.startswith('proc_kill_'):
        pid = callback_data.replace('proc_kill_', '')
        await handle_process_action(query, 'kill', int(pid))
    elif callback_data.startswith('proc_forcekill_'):
        pid = callback_data.replace('proc_forcekill_', '')
        await handle_process_action(query, 'forcekill', int(pid))
    elif callback_data.startswith('proc_suspend_'):
        pid = callback_data.replace('proc_suspend_', '')
        await handle_process_action(query, 'suspend', int(pid))
    elif callback_data.startswith('proc_resume_'):
        pid = callback_data.replace('proc_resume_', '')
        await handle_process_action(query, 'resume', int(pid))
    elif callback_data.startswith('proc_nice_'):
        parts = callback_data.replace('proc_nice_', '').split('_')
        await handle_process_action(query, 'nice', int(parts[0]), int(parts[1]))
    # Chart handlers
    elif callback_data == 'chart_cpu':
        await handle_chart_callback(query, 'cpu')
    elif callback_data == 'chart_memory':
        await handle_chart_callback(query, 'memory')
    elif callback_data == 'chart_disk':
        await handle_chart_callback(query, 'disk')
    elif callback_data == 'chart_network':
        await handle_chart_callback(query, 'network')
    # System commands
    elif callback_data == 'system_info':
        await execute_and_show(query, get_system_info, "💻 SYSTEM INFO", 'menu_system')
    elif callback_data == 'system_cpu':
        await execute_and_show(query, get_cpu_info, "🔥 CPU INFO", 'menu_system')
    elif callback_data == 'system_memory':
        await execute_and_show(query, get_memory_info, "🧠 MEMORY INFO", 'menu_system')
    elif callback_data == 'system_uptime':
        await execute_and_show(query, get_uptime, "⏰ UPTIME", 'menu_system')
    elif callback_data == 'system_processes':
        await execute_and_show(query, get_processes_info, "📊 TOP PROCESSES", 'menu_system')
    elif callback_data == 'system_users':
        await execute_and_show(query, get_users_info, "👥 LOGGED USERS", 'menu_system')
    # Disk commands
    elif callback_data == 'disk_info':
        await execute_and_show(query, get_disk_info, "💾 DISK INFO", 'menu_disk')
    elif callback_data == 'disk_partitions':
        await execute_and_show(query, get_partitions_info, "📂 PARTITIONS", 'menu_disk')
    elif callback_data == 'disk_io':
        await execute_and_show(query, get_disk_io_stats, "💿 DISK I/O", 'menu_disk')
    # Network commands
    elif callback_data == 'network_info':
        await execute_and_show(query, get_network_info, "🌐 NETWORK INFO", 'menu_network')
    elif callback_data == 'network_stats':
        await execute_and_show(query, get_network_stats, "📈 NETWORK STATS", 'menu_network')
    elif callback_data == 'network_publicip':
        await execute_and_show(query, get_public_ip, "🌍 PUBLIC IP", 'menu_network')
    elif callback_data == 'network_connections':
        await execute_and_show(query, get_connections, "🔌 CONNECTIONS", 'menu_network')
    elif callback_data == 'network_routing':
        await execute_and_show(query, get_routing_table, "🛣️ ROUTING TABLE", 'menu_network')
    elif callback_data == 'network_dns':
        await execute_and_show(query, get_dns_info, "🔍 DNS INFO", 'menu_network')
    # Service commands
    elif callback_data == 'service_all':
        await execute_and_show(query, lambda: list_services(), "⚙️ ALL SERVICES", 'menu_service')
    elif callback_data == 'service_running':
        await execute_and_show(query, lambda: list_services('running'), "✅ RUNNING SERVICES", 'menu_service')
    elif callback_data == 'service_failed':
        await execute_and_show(query, lambda: list_services('failed'), "❌ FAILED SERVICES", 'menu_service')
    # Device commands
    elif callback_data == 'device_info':
        await execute_and_show(query, get_device_info, "🔧 DEVICE INFO", 'menu_device')
    elif callback_data == 'device_sensors':
        await execute_and_show(query, get_sensors_info, "🌡️ SENSORS", 'menu_device')
    elif callback_data == 'device_battery':
        await execute_and_show(query, get_battery_info, "🔋 BATTERY", 'menu_device')
    else:
        await query.edit_message_text("❌ Unknown command")


async def execute_and_show(query, func, title, back_menu):
    """Execute function dan show hasil dengan back button"""
    try:
        # Show loading
        await query.edit_message_text(f"⏳ Loading {title}...")
        
        # Execute function
        result = func()
        
        # Add title
        message = f"*{title}*\n\n{result}"
        
        # Create back button
        keyboard = [
            [InlineKeyboardButton("◀️ Back", callback_data=back_menu)],
            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send result (handle long messages)
        if len(message) > 4000:
            chunks = [message[i:i+4000] for i in range(0, len(message), 4000)]
            for i, chunk in enumerate(chunks):
                if i == 0:
                    await query.edit_message_text(
                        chunk,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=None
                    )
                elif i == len(chunks) - 1:
                    await query.message.reply_text(
                        chunk,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=reply_markup
                    )
                else:
                    await query.message.reply_text(
                        chunk,
                        parse_mode=ParseMode.MARKDOWN
                    )
        else:
            await query.edit_message_text(
                message,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
    except Exception as e:
        keyboard = [[InlineKeyboardButton("◀️ Back", callback_data=back_menu)]]
        await query.edit_message_text(
            f"❌ Error: {str(e)}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )



async def show_main_menu(query):
    """Tampilkan main menu"""
    text = """
🤖 *TELEGRAM SYSTEM MONITOR*

Pilih kategori monitoring:
"""
    keyboard = [
        [
            InlineKeyboardButton("💻 System", callback_data='menu_system'),
            InlineKeyboardButton("💾 Disk", callback_data='menu_disk')
        ],
        [
            InlineKeyboardButton("🌐 Network", callback_data='menu_network'),
            InlineKeyboardButton("⚙️ Services", callback_data='menu_service')
        ],
        [
            InlineKeyboardButton("🔧 Device", callback_data='menu_device'),
            InlineKeyboardButton("🛠️ Tools", callback_data='menu_tools')
        ],
        [InlineKeyboardButton("🔄 Refresh", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_system_menu(query):
    """Tampilkan system submenu"""
    text = "💻 *SYSTEM MONITORING*\n\nPilih informasi yang ingin dilihat:"
    keyboard = [
        [
            InlineKeyboardButton("📋 System Info", callback_data='system_info'),
            InlineKeyboardButton("🔥 CPU", callback_data='system_cpu')
        ],
        [
            InlineKeyboardButton("🧠 Memory", callback_data='system_memory'),
            InlineKeyboardButton("⏰ Uptime", callback_data='system_uptime')
        ],
        [
            InlineKeyboardButton("📊 Processes", callback_data='system_processes'),
            InlineKeyboardButton("👥 Users", callback_data='system_users')
        ],
        [InlineKeyboardButton("◀️ Back to Main", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_disk_menu(query):
    """Tampilkan disk submenu"""
    text = "💾 *DISK MONITORING*\n\nPilih informasi yang ingin dilihat:"
    keyboard = [
        [
            InlineKeyboardButton("📊 Disk Usage", callback_data='disk_info'),
            InlineKeyboardButton("📂 Partitions", callback_data='disk_partitions')
        ],
        [
            InlineKeyboardButton("💿 Disk I/O", callback_data='disk_io'),
        ],
        [InlineKeyboardButton("◀️ Back to Main", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_network_menu(query):
    """Tampilkan network submenu"""
    text = "🌐 *NETWORK MONITORING*\n\nPilih informasi yang ingin dilihat:"
    keyboard = [
        [
            InlineKeyboardButton("📡 Interfaces", callback_data='network_info'),
            InlineKeyboardButton("📈 Statistics", callback_data='network_stats')
        ],
        [
            InlineKeyboardButton("🌍 Public IP", callback_data='network_publicip'),
            InlineKeyboardButton("🔌 Connections", callback_data='network_connections')
        ],
        [
            InlineKeyboardButton("🛣️ Routing", callback_data='network_routing'),
            InlineKeyboardButton("🔍 DNS", callback_data='network_dns')
        ],
        [InlineKeyboardButton("◀️ Back to Main", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_service_menu(query):
    """Tampilkan service submenu"""
    text = "⚙️ *SERVICE MANAGEMENT*\n\nPilih kategori service:"
    keyboard = [
        [
            InlineKeyboardButton("📋 All Services", callback_data='service_all'),
        ],
        [
            InlineKeyboardButton("✅ Running", callback_data='service_running'),
            InlineKeyboardButton("❌ Failed", callback_data='service_failed')
        ],
        [InlineKeyboardButton("◀️ Back to Main", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_device_menu(query):
    """Tampilkan device submenu"""
    text = "🔧 *DEVICE INFORMATION*\n\nPilih informasi device:"
    keyboard = [
        [
            InlineKeyboardButton("💻 Hardware", callback_data='device_info'),
            InlineKeyboardButton("🌡️ Sensors", callback_data='device_sensors')
        ],
        [
            InlineKeyboardButton("🔋 Battery", callback_data='device_battery'),
        ],
        [InlineKeyboardButton("◀️ Back to Main", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_tools_menu(query):
    """Tampilkan tools submenu"""
    text = "🛠️ *TOOLS & UTILITIES*\n\nFitur tambahan:"
    keyboard = [
        [
            InlineKeyboardButton("📊 Charts", callback_data='menu_charts'),
            InlineKeyboardButton("🔔 Alerts", callback_data='menu_alerts')
        ],
        [
            InlineKeyboardButton("📝 Reports", callback_data='menu_reports'),
            InlineKeyboardButton("🔧 Processes", callback_data='menu_processes')
        ],
        [
            InlineKeyboardButton("🐳 Docker", callback_data='menu_docker'),
            InlineKeyboardButton("📦 Packages", callback_data='menu_packages')
        ],
        [
            InlineKeyboardButton("🛡️ Firewall", callback_data='menu_firewall'),
            InlineKeyboardButton("📜 Scripts", callback_data='menu_scripts')
        ],
        [
            InlineKeyboardButton("📊 System Logs", callback_data='menu_logs'),
            InlineKeyboardButton("⚙️ Services", callback_data='menu_servicemanager')
        ],
        [
            InlineKeyboardButton("🌐 Network Tools", callback_data='menu_nettools')
        ],
        [InlineKeyboardButton("◀️ Back to Main", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_alerts_menu(query):
    """Show alerts main menu"""
    from src.modules.alerts import alert_manager
    from src.modules.alerts.thresholds import AlertThresholds
    
    thresholds = AlertThresholds()
    active = alert_manager.get_active_alerts()
    
    text = f"""
🔔 *ALERT SYSTEM*

Active Alerts: {len(active)}
Total Metrics: 4 (CPU, Memory, Disk, Swap)

Configure thresholds and monitor system health
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
        [InlineKeyboardButton("◀️ Back to Tools", callback_data='menu_tools')],
        [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_charts_menu(query):
    """Tampilkan charts submenu"""
    text = "📊 *CHARTS & VISUALIZATION*\n\nGenerate visual charts:"
    keyboard = [
        [
            InlineKeyboardButton("🔥 CPU Chart", callback_data='chart_cpu'),
            InlineKeyboardButton("🧠 Memory Chart", callback_data='chart_memory')
        ],
        [
            InlineKeyboardButton("💾 Disk Chart", callback_data='chart_disk'),
            InlineKeyboardButton("🌐 Network Chart", callback_data='chart_network')
        ],
        [InlineKeyboardButton("◀️ Back to Tools", callback_data='menu_tools')],
        [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_help(query):
    """Tampilkan help"""
    text = """
📚 *HELP - CARA PENGGUNAAN*

*Navigasi:*
• Gunakan tombol inline keyboard untuk navigasi
• Tombol "Back" untuk kembali ke menu sebelumnya
• Tombol "Main Menu" untuk kembali ke menu utama

*Kategori:*
• 💻 *System* - CPU, Memory, Uptime, Processes, Users
• 💾 *Disk* - Disk usage, Partitions, I/O Stats
• 🌐 *Network* - Interfaces, Stats, Connections, DNS
• ⚙️ *Services* - Service management & monitoring
• 🔧 *Device* - Hardware info, Sensors, Battery
• 🛠️ *Tools* - Advanced features (coming soon)

*Text Commands:*
Anda juga bisa menggunakan text commands seperti:
`/cpu` `/memory` `/disk` `/network` `/services`

Type `/help` untuk daftar lengkap commands.
"""
    keyboard = [[InlineKeyboardButton("◀️ Back", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def show_about(query):
    """Tampilkan about"""
    text = """
ℹ️ *ABOUT*

*Telegram System Monitor Bot*
Version: 2.0

Bot monitoring sistem Linux/Debian yang powerful dan mudah digunakan.

*Features:*
✅ Real-time monitoring
✅ Interactive inline keyboard
✅ Admin authentication
✅ Modular architecture
✅ Service management
✅ Network tools

*Tech Stack:*
• Python 3.8+
• python-telegram-bot
• psutil
• systemd

*Repository:*
github.com/jhopan/telegram-system-monitor

*License:* MIT License
*Author:* jhopan
"""
    keyboard = [[InlineKeyboardButton("◀️ Back", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

