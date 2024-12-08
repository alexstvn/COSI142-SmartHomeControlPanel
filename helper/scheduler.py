from apscheduler.schedulers.background import BackgroundScheduler
import pytz

def create_scheduler(timezone):
    tz = pytz.timezone(timezone)
    scheduler = BackgroundScheduler(timezone=tz)
    return scheduler