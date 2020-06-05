# -*- coding: utf-8 -*-

# Copyright Colton Riedel (2019)
# License: MIT

import datetime
import urllib.request
from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv
import json
import os

with open('config.json') as configFile:
	CONFIG = json.load(configFile)
satellitedata_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "SatelliteData"))

def generate_csv(sat, time, eol_index, us_inc, num_samples, data):
    satname = str(sat)
    output_filename = os.path.join( satellitedata_path, satname  + '.csv' )

    outfile = open(output_filename, "w")

    line1_index = eol_index + 1
    line2_index = eol_index + 72

    line1 = data[line1_index:line1_index+70].decode()
    line2 = data[line2_index:line2_index+70].decode()

    satellite = twoline2rv(line1, line2, wgs84)

    for i in range(num_samples):
        datestamp = time.strftime("%Y,%m,%d,%H,%M,%S.%f")

        second = float(str(time.second) + "." + str(time.microsecond))

        position, v = satellite.propagate(time.year, time.month, time.day, \
                time.hour, time.minute, second)

        position_string = ","
        if (position[0] > 0):
            position_string += " "
        position_string += str(position[0]) + ","

        while len(position_string) < 16:
            position_string += " "

        if (position[1] > 0):
            position_string += " "

        position_string += str(position[1]) + ","

        while len(position_string) < 31:
            position_string += " "

        if (position[2] > 0):
            position_string += " "

        position_string += str(position[2])

        outfile.write(datestamp + position_string + "\n");

        time = time + datetime.timedelta(microseconds=us_inc)

    outfile.close()

def main():
    url = "https://www.celestrak.com/NORAD/elements/stations.txt"

    try:
        response = urllib.request.urlopen(url)
        print (response)
        data = response.read()
    except:
        print( "  \033[31mError fetching specified TLE file\033[0m")
        exit(1)

    name_index = data.find(str.encode(""))
    eol_index = data.find(str.encode("\n"), name_index)

    start = ("")

    if start.strip() == "":
        time = datetime.datetime.utcnow()
        print( "  \033[36mUsing current system time (UTC): "),time.isoformat(' '),"\033[0m"
    else:
        try:
            time = datetime.datetime.strptime(start.strip(), "%Y %m %d %H %M %S %f")
            print( "  \033[36mParsed start time as: ",time.isoformat(' '), "\033[0m")
        except:
            print( "  \033[31mUnable to parse start time from: ", start)
            print( "        example of suitable input: 2019 01 09 22 05 16 01\033[0m")
            exit(1)

    inc_field = ("min")

    try:
        inc = int("1")
    except:
        print( "  \033[31mUnable to parse value\033[0m")
        exit(1)

    us_inc = inc

    try:
        num_samples = int("10")
    except:
        print( "  \033[31mUnable to parse value\033[0m")
        exit(1)

    print( "\nGetting all SVs")

    while(eol_index < len(data)):
        sat = data[(eol_index-25):eol_index].strip()

        generate_csv(sat, time, eol_index, us_inc, num_samples, data)

        eol_index = eol_index + 71 + 71 + 26

        print( '.'),

    print( "\n\n\033[1;32mFinished\033[0m")

main()
