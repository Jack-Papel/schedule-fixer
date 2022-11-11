"""
The file that actually handles fixing a given iCal file.

:author Jack Papel
"""
from datetime import datetime, timedelta


# See https://en.wikipedia.org/wiki/ICalendar
#
# The lines we need to change:
#
# DTSTAMP:20220825T192700Z
# DTSTART;TZID=America/New_York:20220902T110000
# DTEND;TZID=America/New_York:20220902T115000
# RRULE:FREQ=WEEKLY;UNTIL=20221209

def fix(filepath: str, save_dir: str, days_offset: int, hours_offset: int) -> None:
    """
    Fix the given iCal file.
    :param filepath: The full path to the iCal file
    :param save_dir: The directory to save the fixed file to
    :param days_offset: The number of days to offset the calendar by
    :param hours_offset: The number of hours to offset the calendar by
    """
    with open(filepath) as f, open(save_dir, "w") as f_fixed:
        for line in f:
            if "DTSTAMP" in line:
                line = line[:8] + _fix_date_and_time(line[8:-1], days_offset, hours_offset) + "Z\n"
            elif "DTSTART" in line:
                line = line[:30] + _fix_date_and_time(line[30:], days_offset, hours_offset) + "\n"
            elif "DTEND" in line:
                line = line[:28] + _fix_date_and_time(line[28:], days_offset, hours_offset) + "\n"
            elif "UNTIL" in line:
                index = (line.find("UNTIL=") + 6)
                line = line[:index] + _fix_date(line[index:], days_offset) + "\n"

            f_fixed.write(line)


def _date_from_ical_time(time_str: str) -> datetime:
    """
    Convert an iCal time string to a datetime object.
    :param time_str: The time, as specified in the iCal file
    :return: The datetime object corresponding to the given time
    """
    year = time_str[0:4]
    month = time_str[4:6]
    day = time_str[6:8]
    # Skip the "T" in the middle
    if len(time_str) < 15:
        return datetime.fromisoformat(f"{year}-{month}-{day}")
    hour = time_str[9:11]
    minute = time_str[11:13]
    second = time_str[13:15]
    return datetime.fromisoformat(f"{year}-{month}-{day} {hour}:{minute}:{second}")


def _ical_datetime_from_datetime(t: datetime) -> str:
    """
    Convert a datetime object to an iCal date & time string.
    :param t: The datetime object to convert
    :return: The iCal date & time string corresponding to the given datetime object
    """
    return f"{_ical_date_from_datetime(t)}T{t.hour:02}{t.minute:02}{t.second:02}"


def _ical_date_from_datetime(t: datetime) -> str:
    """
    Convert a datetime object to an iCal date string.
    :param t: The datetime object to convert
    :return: The iCal date string corresponding to the given datetime object
    """
    return f"{t.year:04}{t.month:02}{t.day:02}"


def _fix_date(date_str: str, days_offset: int) -> str:
    """
    Fix the date in the given iCal date string, by offsetting it by the given number of days.
    :param date_str: The iCal date string to fix
    :param days_offset: The number of days to offset the date by
    :return: The fixed iCal date string
    """
    class_time = _date_from_ical_time(date_str)
    class_time -= timedelta(days=days_offset)
    return _ical_date_from_datetime(class_time)


def _fix_date_and_time(time_str: str, days_offset: int, hours_offset: int) -> str:
    """
    Fix the date and time in the given iCal date & time string, by offsetting it by the given number of days and hours.
    :param time_str: The iCal date & time string to fix
    :param days_offset: The number of days to offset the date by
    :param hours_offset: The number of hours to offset the time by
    :return: The fixed iCal date & time string
    """
    class_time = _date_from_ical_time(time_str)
    class_time -= timedelta(days=days_offset, hours=hours_offset)
    return _ical_datetime_from_datetime(class_time)
