# monitor_utils.py
# Utility functions for monitoring system changes
import psutil

def list_processes():
    return [(p.pid, p.name()) for p in psutil.process_iter()]

def get_resource_usage():
    return {
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent
    }
