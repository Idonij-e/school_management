# pip install apscheduler

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_token_refresh

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_token_refresh, 'interval', minutes=5)
    scheduler.start()