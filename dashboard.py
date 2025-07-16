# dashboard.py
# Functions for displaying system health and security status
from monitor_utils import get_resource_usage

def show_dashboard():
    usage = get_resource_usage()
    print("System Health Dashboard:")
    print(f"CPU Usage: {usage['cpu_percent']}%")
    print(f"Memory Usage: {usage['memory_percent']}%")
    print(f"Disk Usage: {usage['disk_percent']}%")
