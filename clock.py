from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, time
from pytz import timezone
import subprocess

# Define the timezone
finland_timezone = timezone('Europe/Helsinki')

def my_task():
    # Run table.py using subprocess
    subprocess.run(['python', 'table.py'])

def start_task():
    # Run the task immediately
    print("Starting task...")
    my_task()

def stop_task():
    # Stop the task
    print("Stopping task...")
    scheduler.remove_all_jobs()

# Create a scheduler
scheduler = BlockingScheduler(timezone=finland_timezone)

# Schedule start and stop tasks
scheduler.add_job(start_task, 'date')
scheduler.add_job(stop_task, 'cron', day_of_week='mon-fri', hour='22', minute='0')
scheduler.add_job(stop_task, 'cron', day_of_week='mon-fri', hour='23', minute='0')
scheduler.add_job(stop_task, 'cron', day_of_week='mon-fri', hour='0', minute='0')
scheduler.add_job(stop_task, 'cron', day_of_week='sat-sun', hour='*', minute='0')

try:
    # Start the scheduler
    scheduler.start()
except KeyboardInterrupt:
    # Stop the scheduler if Ctrl+C is pressed
    pass