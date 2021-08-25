import schedule
import time

def job():
    print("I'm working...")

# Run job every 3 second/minute/hour/day/week,
# Starting 3 second/minute/hour/day/week from now
schedule.every(1).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
