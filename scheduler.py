import schedule
import time
import sys
import datetime
import calcorbit
import pyorbital
from urllib import error
import logging


def print_usage():
    print("python3 -c [satName] [%dd/%mm/%yy_%HH:%MM:%SS]")


def update_sat_data():
    logging.info("Updating satellite's data")
    try:
        pyorbital.tlefile.fetch("tle.txt")
    except error.URLError:
        message = "Could not download tle data"
        logging.warning(message)
        raise error.URLError(message)


def start_tracking_procedures(sat_name, updating_job):
    """ Starts all procedures related to the sat tracking per se.
    Runs initializers, tries to download latest data about the satellite,
    connects to the Arduino through serial communication.

    :updating_job: the updating data job which was executing until now
    
    :return: the current job already canceled
    """

    logging.info("Tracking procedures for " + sat_name + " in progress")
    # schedule.cancel_job(updating_job)

    for i in range(3):
        try:
            update_sat_data()
            break
        except error.URLError as url_error:
            print(url_error.reason)

    calcorbit.init_tracking(sat_name, reservation_datetime)
    return schedule.CancelJob


def schedule_start(sat_name, reservation_time, updating_job):
    """ Scheduler for the beginning of the satellite tracking procedures

    :reservation time: datetime of the booked time for using the ground station 
    :updating_job: the job which updates the data for the satellite
    """

    logging.info("Satellite's tracking scheduled")

    # schedule the start 3 minutes prior to the event in order to try to download the tle files
    new_reservation_time = reservation_time - datetime.timedelta(seconds=3)
    reservation_time_str = new_reservation_time.strftime("%H:%M:%S")
    schedule.every().day.at(reservation_time_str).do(start_tracking_procedures, sat_name, updating_job)


def schedule_downloads():
    """ Schedules the downloads of the information for the satellite
    to repeat once a week until the beginning of the event

    :return: the scheduling job
    """
    # try:
    return schedule.every(10).seconds.do(update_sat_data)
    # except error.URLError as err:
    #     print("Could not download tle data")
        # raise error.URLError("Could not download tle data")
        # return job


def schedule_job(job, delay_between_jobs):
    return schedule.every(delay_between_jobs).seconds.do(job)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s     %(levelname)s:%(message)s', level=logging.DEBUG)
    # default satellite for tracking - QMR-KWT
    sat_name = 'QMR-KWT'
    # default reservation time - now + 1 min
    reservation_datetime = datetime.datetime.now() + datetime.timedelta(seconds=10)

    print(len(sys.argv))

    if len(sys.argv) >= 3:
        sat_name = sys.argv[2]
        reservation_datetime = datetime.datetime.strptime(sys.argv[3], '%d/%m/%y_%H:%M:%S')

    print(sat_name)
    print(reservation_datetime)

    updating_job = schedule_downloads()
    schedule_start(sat_name, reservation_datetime, updating_job)

    while True:
        schedule.run_pending()
        time.sleep(1)
