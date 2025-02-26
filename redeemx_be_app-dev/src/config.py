from apscheduler.schedulers.background import BackgroundScheduler
import requests

from main import app

API_URL = "http://127.0.0.1:8001/api/v1/user/process/all/transactions"

def process_transactions():
    try:
        response = requests.post(API_URL)
        print("Scheduled Task Executed:", response.status_code, response.json())
    except Exception as e:
        print("Error in Scheduled Task:", e)

scheduler = BackgroundScheduler()
scheduler.add_job(
    process_transactions,
    "cron",
    day_of_week="mon-sat",
    hour=16,
    minute=27 
)
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    print("Shutting down scheduler...")
    scheduler.shutdown()
