#!/usr/bin/env python3
from __future__ import print_function
import os
import sys
from os import listdir
from os.path import isfile, join
import json
import csv
import array
import fileinput
import re
import time

green = (52, 235, 64, 50)
red = (235, 52, 52, 50)
orange = (235, 159, 52, 50)
slope = 8

def colourFromPoints( p1, p2 ):
	altDifference = p1[2] - p2[2]

	if altDifference > slope:
		color = list(map(int, red)) # red
		##print("descending")
	elif altDifference < -slope:
		color = list(map(int, green)) # green
		##print("ascending")
	else:
		color = list(map(int, orange)) # orange
		##print("level flight")

	return color

now = int( time.time() )
# now = int(1589432155)
# print (now)
with open('config.json') as configFile:
	CONFIG = json.load(configFile)


oldestTail= now - CONFIG['opensky']['tailTime']
activeFlightFile = open( CONFIG['opensky']['active'], 'r' )
flightDataPath = CONFIG['opensky']['dataFolder']


czmlHeader = {
		'id': 'document',
		'name': 'CZML Flight Path',
		'version': '1.0'
	},
# Put the data in a list 
flightList = list(czmlHeader) 

for flightLine in activeFlightFile:
	#print(flightLine)
	flightData = flightLine.split(',')
	icao24 = flightData[1]
	flightTime = int(flightData[0])
	timeDiff = oldestTail - flightTime
	# if ( timeDiff>0 ):
	# 	#print('tail to old')
	# 	continue

	flightFile=os.path.join( flightDataPath, icao24 + ".csv" )
	with open(flightFile, 'r') as flight_csv:
		cartDegree = list()
		flightPoints = list()
		flight_reader = csv.reader(flight_csv)
		line_count = 0
		lastPoint = (0,0,0)
		for row in flight_reader:
			if line_count == 0:
				flightID = row[0]
				flightName = row[1]
				line_count +=1
			else:
				pathTime = int( row[0] )
				timeDiff = oldestTail - pathTime
				# print(timeDiff)
				if ( timeDiff<0 ):
					thisPoint = ( float( row[2] ), float( row[1] ), float( row[3] ) )
					if (lastPoint != thisPoint):
						flightPoints.append (thisPoint)
						cartDegree.append (float(row[2]))
						cartDegree.append (float(row[1]))
						cartDegree.append (float(row[3]))
					lastPoint = thisPoint
					line_count +=1
				else:
					continue
	if(len(flightPoints) > 0):
		pass
	else:
		print( flightID, 'not active?')
		continue
	if(len(flightPoints) > 1):
		lineColor = colourFromPoints( flightPoints[ len(flightPoints) -2], flightPoints[ len(flightPoints) -1] )
	else:
		lineColor = (100, 149, 237, 255)	
	cartDegreeJSON = list(map(float, cartDegree))		
	flightLabel = str("This is the flight label for flight ID: " + flightID)		
	# Flights is JSON format for CZML 
	# print(flightID)
	# print(flightName)
	Flights = {
		"id": flightID,
		"name": flightName,
		"polyline": {
			"positions": {
				"cartographicDegrees":	cartDegreeJSON							
			},
			"material": {
				"polylineGlow": {
					"color": {
						"rgba": lineColor
					},
					"glowPower": 0.2,
					"taperPower": 0.3
					}
				},
				"width": 25
			},
				
	}
	Labels = {
		"id": flightName,
		"name": flightName,
		"description": flightLabel,
		
		"label": {
			"text": flightName,
			"font": "11pt Lucida Console",
			"showBackground": "true",
			"backgroundColor": {
				"rgba": [169,169,169,169],
			},
			"fillColor": {
				"rgba": [255, 255, 255, 255],
			},
    	},	
		"position": {
			"cartographicDegrees": 
				lastPoint
			
		}
	}
	flightList.append(Flights) #append the current Flight into the flightList
	flightList.append(Labels)

with open('FlightPath.czml','w') as tempczml:
	json.dump(flightList,tempczml,indent=4)
print("Finished printing Flight Path CZML")
# ------------------------------- SATELLITE DATA BELOW --------------------------------------
oldestTail= now - CONFIG['satellite']['tailTime']
activeFile = open( CONFIG['satellite']['active'], 'r' )
satDataPath = CONFIG['satellite']['dataFolder']

czmlHeader = {
		'id': 'document',
		'name': 'CZML Satellite Path',
		'version': '1.0'
	},
# Put the data in a list 
satList = list(czmlHeader) 

for satLine in activeFile:
	#print(satLine)
	satData = satLine.split(',')
	satName = satData[1]
	satTime = int(satData[0])
	timeDiff = oldestTail - satTime
	# if ( timeDiff>0 ):
	# 	#print('tail to old')
	# 	continue

	satFile=os.path.join( satDataPath, satName + ".csv" )
	with open(satFile, 'r') as sat_csv:
		cartDegree = list()
		satPoints = list()
		sat_reader = csv.reader(sat_csv)
		line_count = 0
		lastPoint = (0,0,0)
		for row in sat_reader:
			pathTime = int( row[0] )
			timeDiff = oldestTail - pathTime
			# print(timeDiff)
			thisPoint = ( float( row[2] ), float( row[1] ), float( row[3] ) )
			# print(thisPoint)
			if (lastPoint != thisPoint):
				satPoints.append (thisPoint)
				cartDegree.append (float(row[2]))
				cartDegree.append (float(row[1]))
				cartDegree.append (float(row[3]))
			lastPoint = thisPoint
			line_count +=1
	if(len(satPoints) > 0):
		pass
	else:
		print( satName, 'not active?')
		continue
	if(len(satPoints) > 1):
		lineColor = (100, 149, 237, 255)
	else:
		lineColor = (100, 149, 237, 255)	
	cartDegreeJSON = list(map(float, cartDegree))		
	satLabel = str("This is the satellite label for satellite: " + satName)		
	# Satellite is JSON format for CZML 
	
	Satellite = {
		"id": satName,
		"name": satName,
		"polyline": {
			"positions": {
				"cartographicDegrees":	cartDegreeJSON							
			},
			"material": {
				"polylineGlow": {
					"color": {
						"rgba": lineColor
					},
					"glowPower": 0.2,
					"taperPower": 0.3
					}
				},
				"width": 10
			},
				
	}
	Labels = {
		"id": satName,
		"name": satName,
		"description": satLabel,
		
		"label": {
			"text": satName,
			"font": "11pt Lucida Console",
			"showBackground": "true",
			"backgroundColor": {
				"rgba": [169,169,169,169],
			},
			"fillColor": {
				"rgba": [255, 255, 255, 255],
			},
    	},	
		"position": {
			"cartographicDegrees": 
				lastPoint
			
		}
	}
	satList.append(Satellite) #append the current Flight into the satList
	satList.append(Labels)

with open('SatellitePath.czml','w') as tempczml:
	json.dump(satList,tempczml,indent=4)
print("Finished printing Satellite Path CZML")