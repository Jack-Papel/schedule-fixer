from datetime import datetime, timedelta
from schedule_fixer import fs_util


# See https://en.wikipedia.org/wiki/ICalendar
#
# The lines we need to change:
#
# DTSTAMP:20220825T192700Z
# DTSTART;TZID=America/New_York:20220902T110000
# DTEND;TZID=America/New_York:20220902T115000
# RRULE:FREQ=WEEKLY;UNTIL=20221209

def fix(filepath, days_offset, hours_offset):
    # Consider allowing specifying the copy path?
    with open(filepath) as f, open(fs_util.fixed_path(filepath), "w") as fcopy:
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

            fcopy.write(line)


def _date_from_ical_time(time_str: str) -> datetime:
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
    return f"{_ical_date_from_datetime(t)}T{t.hour:02}{t.minute:02}{t.second:02}"


def _ical_date_from_datetime(t: datetime) -> str:
    return f"{t.year:04}{t.month:02}{t.day:02}"


def _fix_date(date_str: str, days_offset) -> str:
    class_time = _date_from_ical_time(date_str)
    class_time -= timedelta(days=days_offset)
    return _ical_date_from_datetime(class_time)


def _fix_date_and_time(time_str: str, days_offset, hours_offset) -> str:
    class_time = _date_from_ical_time(time_str)
    class_time -= timedelta(days=days_offset, hours=hours_offset)
    return _ical_datetime_from_datetime(class_time)
