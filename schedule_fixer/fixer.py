import datetime


def fix(filepath, days_offset, hours_offset):
    with open(filepath) as f:
        for line in f:
            print(line)
            # TODO fix calendar
