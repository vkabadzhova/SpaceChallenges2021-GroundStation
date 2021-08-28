import schedule
import time
import sys
import datetime
import calcorbit
import pyorbital

def print_usage():
    print("python3 -c [satName] [%dd/%mm/%yy_%HH:%MM:%SS]")


def update_sat_data():
    print("updating data job")
    pyorbital.tlefile.fetch("tle.txt")


def start_tracking_procedures(updating_job):
    """ Starts all procedures related to the sat tracking per se.
    Runs initializers, tries to download latest data about the satellite,
    connects to the Arduino through serial communication.

    :updating_job: the updating data job which was executing until now
    
    :return: the current job already canceled
    """

    print("Start tracking procedures in progress")
    schedule.cancel_job(updating_job)
    
    is_updated_successfully = False
    while not is_updated_successfully:
        try:
            update_sat_data()
            is_update_successfully = True
        except Exception as exc:
            print(exc)

    calcorbit.init_tracking()
    return schedule.CancelJob


def schedule_start(reservation_time, updating_job):
    """ Scheduler for the beginning of the satellite tracking procedures

    :reservation time: datetime of the booked time for using the ground station 
    :updating_job: the job which updates the data for the satellite
    """
    # schedule the start 3 minutes prior to the event in order to try to download the tle files
    new_reservation_time = reservation_time - datetime.timedelta(seconds=3) 
    reservation_time_str = new_reservation_time.strftime("%H:%M:%S")
    schedule.every().day.at(reservation_time_str).do(start_tracking_procedures, updating_job)


def schedule_downloads():
    """ Schedules the downloads of the information for the satellite
    to repeat once a week until the beginning of the event

    :return: the scheduling job
    """
    return schedule.every(2).seconds.do(update_sat_data)


if __name__ == "__main__":
    # default satellite for tracking - QMR-KWT
    sat_name = 'QMR-KWT'
    # default reservation time - now + 1 min
    reservation_datetime = datetime.datetime.now() + datetime.timedelta(seconds=10) 

    print(len(sys.argv)) 

    if (len(sys.argv) >= 3):
        sat_name = sys.argv[2]
        reservation_datetime = datetime.datetime.strptime(sys.argv[3], '%d/%m/%y_%H:%M:%S')
    
    print(sat_name)
    print(reservation_datetime)

    updating_job = schedule_downloads()
    schedule_start(reservation_datetime, updating_job)

    while True:
        schedule.run_pending()
        time.sleep(1)

