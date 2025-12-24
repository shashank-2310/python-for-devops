"""Task: Create a Python script that:
    Takes threshold values (CPU, disk, memory) from user input
    Also fetches system metrics using a Python library (example: psutil)
    Compares metrics against thresholds
    Prints the result to the terminal
"""
import os
import sys

try:
    import psutil
except ImportError:
    print("psutil is not installed. Install with: pip install psutil")
    sys.exit(1)


# Function to take threshold values from user as input
def get_thresholds():
    try:
        cpu_threshold = int(input("\nEnter CPU Threshold(%): "))
        disk_threshold = int(input("\nEnter Disk Threshold(%): "))
        mem_threshold = int(input("\nEnter Memory Threshold(%): "))
    except ValueError:
        print("Invalid input. Please enter integer values for thresholds.")
        sys.exit(1)
    except (KeyboardInterrupt, EOFError):
        print("\nInput cancelled by user.")
        sys.exit(0)

    # Validate ranges
    for name, val in (("CPU", cpu_threshold), ("Disk", disk_threshold), ("Memory", mem_threshold)):
        if not (0 <= val <= 100):
            print(f"Invalid {name} threshold: {val}. Must be between 0 and 100.")
            sys.exit(1)

    return cpu_threshold, disk_threshold, mem_threshold


# Function to compare metrics against thresholds
def check_system_health():
    # Get threshold values
    try:
        cpu_threshold, disk_threshold, mem_threshold = get_thresholds()
    except Exception as e:
        print(f"check_system_health: failed to get thresholds: {e}")
        sys.exit(1)

    # Fetch current system metrics
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        root_path = os.path.abspath(os.sep)
        disk_usage = psutil.disk_usage(root_path).percent
        mem_usage = psutil.virtual_memory().percent
    except (psutil.Error, PermissionError) as e:
        print(f"check_system_health: failed to fetch system metrics: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"check_system_health: unexpected error fetching metrics: {e}")
        sys.exit(1)

    print("\n========== System Metrics ==========\n")
    def report(name: str, value, threshold, unit: str = "%"):
        if value is None:
            print(f"{name}: metric unavailable\n")
            return
        if value > threshold:
            print(f"Alert: HIGH {name} usage (>{threshold}{unit}): {value}{unit}\n")
        else:
            print(f"Safe: {name} usage within limits (<{threshold}{unit}): {value}{unit}\n")

    report("CPU", cpu_usage, cpu_threshold)
    report("Disk", disk_usage, disk_threshold)
    report("Memory", mem_usage, mem_threshold)


if __name__ == "__main__":
    try:
        check_system_health()
    except Exception as e:
        print(f"Main: unexpected error: {e}")
        sys.exit(1)
