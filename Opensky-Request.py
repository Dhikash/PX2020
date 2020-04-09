#!/usr/bin/env python3

import requests
import json
import os
import sys
import time
from os.path import expanduser as ospath
import fcntl

with open('config.json') as configFile:
	CONFIG = json.load(configFile)

with open('center.json') as centerFile:
	CENTER = json.load( centerFile )

now = int( time.time() )
#print(CENTER['timestamp'], now)

if (CENTER['timestamp'] < (now - CONFIG['centerExpiry']) ):
	print( sys.argv[0],"center timestamp old, no one watching, abort." )
	quit(-1)

# calculate NSEW boundaries for viewbox
bboxSize = CONFIG['bboxSize']
lamin = round( CENTER['lat'] - bboxSize, 1)
lamax = round( CENTER['lat'] + bboxSize, 1)
lomin = round( CENTER['lon'] - bboxSize * 1.5, 1)
lomax = round( CENTER['lon'] + bboxSize * 1.5, 1)

# Sydney query hard-code
# response = requests.get("https://opensky-network.org/api/states/all?lamin=-35&lomin=149&lamax=-32.5&lomax=153")

apiCredentials = CONFIG['opensky']['apiKey'] + '@'

requestURL = "https://" + apiCredentials + "opensky-network.org/api/states/all?lamin=" + str(lamin) + "&lomin="+str(lomin) + "&lamax="+ str(lamax) + "&lomax=" + str(lomax)

print( requestURL )

requestStartTime = time.time()

response = requests.get( requestURL )

requestDuration = round( 1000* (time.time() - requestStartTime))

#print(response.json())

opensky = response.json()

if opensky["states"] is None:
  print("no flight states found")
  exit()

timestamp = opensky['time']
flights = opensky['states']

flightdata_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "FlightData"))

activeFile = open('Active/opensky.csv', 'w')
fcntl.flock( activeFile, fcntl.LOCK_EX | fcntl.LOCK_NB )

print('flights %d request took %dms' % (len(flights), requestDuration) )

for flight in flights:
		
	altitude=flight[13]
	if altitude is None:
		continue

	icao24=flight[0]
	flightNo=flight[1].rstrip()
	longitude=flight[5]
	latitude=flight[6]
	altitude=int(altitude)
 
#	if (flightNo == ""): # if flightNo empty use icao24
#		flightNo = '(' + icao24 + ')'
#		print('No flightNo', flightNo)

	filepath = os.path.join( flightdata_path, icao24 + '.csv' )
	# print(filepath)
	exists = os.path.isfile( filepath )

	if exists:
		with open( filepath, 'a' ) as dataFilee:
			fcntl.flock( dataFilee, fcntl.LOCK_EX | fcntl.LOCK_NB )
			dataFilee.write( "%s,%s,%s,%s\n" % (timestamp,latitude,longitude,altitude) )
			fcntl.flock( dataFilee, fcntl.LOCK_UN )
			dataFilee.close()
	else:
		# print("New file")
		with open( filepath, 'w' ) as dataFilee:
			fcntl.flock( dataFilee, fcntl.LOCK_EX | fcntl.LOCK_NB )
			dataFilee.write( "%s,%s\n" % ( icao24,flightNo) )
			dataFilee.write( "%s,%s,%s,%s\n" % (timestamp,latitude,longitude,altitude) )
			fcntl.flock( dataFilee, fcntl.LOCK_UN )
			dataFilee.close()

	activeFile.write( "%s,%s,%s,%s\n" % (timestamp,icao24,latitude,longitude) )
			
fcntl.flock( activeFile, fcntl.LOCK_UN )
activeFile.close()
