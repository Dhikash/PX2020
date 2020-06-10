#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright Colton Riedel (2019)
# License: MIT
# modified by Eamon Spillane
import datetime
import time
import urllib.request
from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv
import json
import os
import requests
import sys
import pyproj
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
with open('config.json') as configFile:
	CONFIG = json.load(configFile)
satellitedata_path = os.path.abspath(os.path.join(os.path.dirname(__file__), CONFIG['satellite']['dataFolder']))
activeFile = open('Active/celestrak.csv', 'w')
def converttolla(x, y, z):
    x = x*1000
    y = y*1000
    z = z*1000
    ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
    lon, lat, alt = pyproj.transform(ecef, lla, x, y, z, radians=False)
    
    return  (lon, lat, alt)

def generate_csv(sat, sattime, eol_index, us_inc, num_samples, data):
    satname = str(sat.decode("utf-8"))
    if (satname == "ISS DEB"):
        return()
    output_filename = os.path.join(satellitedata_path, satname  + '.csv' )
    datasssss = str(data)
    # print (datasssss)
    outfile = open(output_filename, "a")

    line1_index = eol_index + 1
    line2_index = eol_index + 72

    line1 = data[line1_index:line1_index+70].decode()
    line2 = data[line2_index:line2_index+70].decode()

    satellite = twoline2rv(line1, line2, wgs84)

    for i in range(num_samples):
        datestamp = sattime.strftime("%Y,%m,%d,%H,%M,%S")
        second = int(sattime.second)
        timestamp = str(int(time.mktime(datetime.datetime.strptime(datestamp, "%Y,%m,%d,%H,%M,%S").timetuple())))
        # print(timestamp)
        position, v = satellite.propagate(sattime.year, sattime.month, sattime.day, \
                sattime.hour, sattime.minute, second)
        
        lla = (converttolla(position[0], position[1], position[2]))
        

        position_string = (", " + str(lla[1]) + ", " + str(lla[0]) + ", "+ str(int(lla[2])))
        # test = (", " + str(position[0]) + ", " + str(position[1]) + ", "+ str(position[2]))
        outfile.write(timestamp + position_string  + "\n")
        activeFile.write("%s,%s" % (timestamp,satname ) + position_string + "\n")
        sattime = sattime + datetime.timedelta(microseconds=us_inc)
    outfile.close()
    
def main():
    url = "https://www.celestrak.com/NORAD/elements/stations.txt"

    try:
        response = urllib.request.urlopen(url)
        # print (response)
        data = response.read()
    except:
        print( "  \033[31mError fetching specified TLE file\033[0m")
        exit(1)

    name_index = data.find(str.encode(""))
    eol_index = data.find(str.encode("\n"), name_index)

    start = ("")

    if start.strip() == "":
        time = datetime.datetime.utcnow()
        # print( "  \033[36mUsing current system time (UTC): "),time.isoformat(' '),"\033[0m"
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
        num_samples = int("1")
    except:
        print( "  \033[31mUnable to parse value\033[0m")
        exit(1)

    print( "\nFetching satellites data")
    counter = int(0)
    prevsat = str()
    while(eol_index < len(data)):
        sat = data[(eol_index-25):eol_index].strip()
        
        generate_csv(sat, time, eol_index, us_inc, num_samples, data)

        eol_index = eol_index + 71 + 71 + 26
        counter += 1
        if (counter == 20):
            break
        # print( '.'),
    
    print( 'Fetched %d satellite requests\n' % counter)
    activeFile.close()
main()
