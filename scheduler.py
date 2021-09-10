import os
import tempfile
import schedule
import time
import sys
import datetime
import calcorbit
import manage_bookings
import pyorbital
from urllib import error
import logging


def print_usage():
    print("python3 -c [satName] [%dd/%mm/%yy_%HH:%MM:%SS]")


def update_sat_data():
    logging.debug("Updating tle")
    try:
        tmp_tle_filename = tempfile.NamedTemporaryFile().name
        pyorbital.tlefile.fetch(tmp_tle_filename)
        logging.info("TLE successfully updated")
        tle_genuine_filename = "tle.txt"
        os.replace(tmp_tle_filename, tle_genuine_filename)
        logging.debug(tmp_tle_filename + " successfully renamed to " + tle_genuine_filename + " - Information updated")
    except error.URLError as err:
        message = "Could not update TLE file - " + str(err)
        logging.warning(message)


def update_booking_data(path_to_json_files):
    logging.debug("Updating bookings")
    bookings = manage_bookings.read_bookings(path_to_json_files)
    for booking in bookings:
        schedule_start(calcorbit.norad_to_name(booking['norad_id']),booking['start_time'])


def start_tracking_procedures(sat_name):
    """ Starts all procedures related to the sat tracking per se.
    Runs initializers, tries to download latest data about the satellite,
    connects to the Arduino through serial communication.

    :updating_job: the updating data job which was executing until now
    
    :return: the current job already canceled
    """

    logging.info("Tracking procedures for " + sat_name + " in progress")

    update_sat_data()

    calcorbit.init_tracking(sat_name, reservation_datetime)
    return schedule.CancelJob


def schedule_start(sat_name, reservation_time):
    """ Scheduler for the beginning of the satellite tracking procedures

    :sat_name: the name of the satellite to be tracked, e.g. "QMR-KWT"
    :reservation time: datetime of the booked time for using the ground station 
    """

    logging.info("Satellite's tracking scheduled")

    # schedule the start 3 minutes prior to the event in order to try to download the tle files
    new_reservation_time = reservation_time - datetime.timedelta(seconds=3)
    reservation_time_str = new_reservation_time.strftime("%H:%M:%S")
    schedule.every().day.at(reservation_time_str).do(start_tracking_procedures, sat_name)


def schedule_downloads():
    """ Schedules the update of the tle file - once a week

    :return: the scheduling job
    """

    schedule.every(10).seconds.do(update_sat_data)
    logging.info("Updating TLE scheduled")



def schedule_booking(path):
    """ Schedules the reading of the bookings once a week

    :return: the scheduling job
    """
    schedule.every(10).seconds.do(update_booking_data, path)
    logging.info("Updating Bookings scheduled")


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s     %(levelname)s:%(message)s', level=logging.DEBUG)

    # default satellite for tracking - QMR-KWT
    sat_name = 'QMR-KWT'

    # default reservation time - now + 1 min
    reservation_datetime = datetime.datetime.now() + datetime.timedelta(seconds=20)

    print(len(sys.argv))

    if len(sys.argv) >= 3:
        sat_name = sys.argv[2]
        reservation_datetime = datetime.datetime.strptime(sys.argv[3], '%d/%m/%y_%H:%M:%S')

    print(sat_name)
    print(reservation_datetime)

    schedule_downloads()
    schedule_booking('../API/')
    schedule_start(sat_name, reservation_datetime)

    while True:
        schedule.run_pending()
        time.sleep(1)
