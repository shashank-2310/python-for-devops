''''
Task: Create a Python script that:
    Takes threshold values (CPU, disk, memory) from user input
    Also fetches system metrics using a Python library (example: psutil)
    Compares metrics against thresholds
    Prints the result to the terminal
'''
import psutil

# Function to take threshold values from user as input
def get_thresholds():

    cpu_threshold = int(input("\nEnter CPU Threshold(%): "))
    disk_threshold = int(input("\nEnter Disk Threshold(%): "))
    mem_threshold = int(input("\nEnter Memory Threshold(%): "))

    return cpu_threshold, disk_threshold, mem_threshold

# Function to compare metrics against thresholds
def check_system_health ():

    # Get threshold values
    cpu_threshold, disk_threshold, mem_threshold = get_thresholds()

    # Fetch current sytem metrics
    cpu_usage = psutil.cpu_percent(interval=1)
    disk_usage = psutil.disk_usage("/").percent
    mem_usage = psutil.virtual_memory().percent

    print("\n========== System Metrics ==========\n")
    
    # CPU check
    if cpu_usage > cpu_threshold:
        print(f"Alert: HIGH CPU usage (>{cpu_threshold}%): {cpu_usage}%\n")
    else:
        print(f"Safe: CPU usage within limits (<{cpu_threshold}%): {cpu_usage}%\n")

    # Disk check
    if disk_usage > disk_threshold:
        print(f"Alert: HIGH Disk usage (>{disk_threshold}%): {disk_usage}%\n")
    else:
        print(f"Safe: Disk usage within limits (<{disk_threshold}%): {disk_usage}%\n")

    # Memory check
    if mem_usage > mem_threshold:
        print(f"Alert: HIGH Memory usage (>{mem_threshold}%): {mem_usage}%\n")
    else:
        print(f"Safe: Memory usage within limits (<{mem_threshold}%): {mem_usage}%\n")

check_system_health()


