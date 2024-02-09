from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, time
from pytz import timezone

# Define the timezone
finland_timezone = timezone('Europe/Helsinki')

def my_task():
    # Put your task logic here
    print('starting table.py')
    subprocess.run(['python', 'table.py'])

# Create a scheduler
scheduler = BlockingScheduler(timezone=finland_timezone)

# Define the job
scheduler.add_job(
    my_task,
    'cron',
    day_of_week='mon-fri',  # Run on weekdays
    hour='9-22',             # Run from 9 AM to 10 PM
    minute='0',              # Run at the beginning of the hour
)

try:
    # Start the scheduler
    print('Scheduler starting.')
    scheduler.start()
    print('Scheduler started.')
except KeyboardInterrupt:
    # Stop the scheduler if Ctrl+C is pressed
    pass