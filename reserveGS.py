import schedule
import time
import sys
from datetime import datetime


def print_usage():
    print("python3 -c [satName] [%dd/%mm/%yy_%HH:%MM:%SS]")

def exec_reservation_job():
    pass

def update_sat_data():
    print("updating data job")

def schedule_start():
    pass

def schedule_downloads():
    schedule.every(2).seconds.do(update_sat_data)

if __name__ == "__main__":
    sat_name = 'QMR-KWT'
    reservation_time='08/08/08_18:56:36' 
    print(len(sys.argv)) 

    if len(sys.argv) >= 2: 
        sat_name = sys.argv[1]
        reservation_time = datetime.strptime(sys.argv[2], '%d/%m/%y_%H:%M:%S')
        print(sat_name)
        print(reservation_time)
    else:
        print_usage()
        exit(1)


    schedule_start()
    schedule_downloads()

    while True:
        schedule.run_pending()
        time.sleep(1)
