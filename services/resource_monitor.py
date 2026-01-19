# services/resource_monitor.py

import time
import psutil


def print_usage(tag: str = ""):
    vm = psutil.virtual_memory()
    print(
        f"[{tag}] CPU: {psutil.cpu_percent(interval=0.2)}% | "
        f"RAM: {vm.percent}% | "
        f"Libre: {round(vm.available / 1024 / 1024, 1)} MB"
    )