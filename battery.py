

from __future__ import print_function
import sys

import psutil


def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%02d:%02d:%02d" % (hh, mm, ss)


def battery():
    if not hasattr(psutil, "sensors_battery"):
        return sys.exit("platform not supported")
    batt = psutil.sensors_battery()
    if batt is None:
        return sys.exit("no battery is installed")

    print("my Battery is at:     %s%%" % round(batt.percent, 2))
    if batt.power_plugged:
        print("I am plugged in")
        print("and:     %s" % (
            "charging" if batt.percent < 100 else "fully charged"))

    else:
        print("My battery is at:       %s" % secs2hours(batt.secsleft))
        print("My Battery is:     %s" % "discharging")
        print("I am not connected to a power source")


if __name__ == '__main__':
    battery()
