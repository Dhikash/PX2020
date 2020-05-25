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

flightdir = 'C:\\Users\\dhika\\Documents\\Convert\\Flights'
csvID = os.listdir(flightdir)
number_of_flights = len(csvID)
print(csvID)

green = (52, 235, 64, 1)
red = (235, 52, 52, 1)
orange = (235, 159, 52, 1)

czmlHeader = {
		'id': 'document',
		'name': 'CZML Flight Path Test',
		'version': '1.0'
	},
# Put the data in a list 
flightList = list(czmlHeader) 



# For loop that reads all csv files
for x in range(number_of_flights):
	with open(flightdir+"\\"+csvID[x], 'r') as flight_csv:
		cartDegree = list()
		flight_reader = csv.reader(flight_csv)
		line_count = 0
		for row in flight_reader:
			if line_count == 0:
				flightID = row[0]
				flightName = row[1]
				line_count +=1
			else:
				cartDegree.append (row[2])
				cartDegree.append (row[1])
				cartDegree.append (row[3])
				line_count +=1
		cartDegreeFloat = list(map(float, cartDegree))		
	#Flights is JSON format for CZML 
	# print(flightID)
	# print(flightName)
	Flights = {
		"id": flightID,
		"name": flightName,
		"polyline": {
			"positions": {
				"cartographicDegrees":[	
					cartDegreeFloat			
					]
			},
			"material": {
				"polylineGlow": {
					"color": {
						"rgba": [100, 149, 237, 255]
					},
					"glowPower": 0.2,
					"taperPower": 0.3
					}
				},
				"width": 10
			},
				
	}
	Labels = {
		"id": flightName,
		"name": flightName,
		"description": "The flight label",
		
		"label": {
			"text": flightName[0],
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
			"cartographicDegrees": [
			]
		}
	}
	flightList.append(Flights) #append the current Flight into the flightList
	flightList.append(Labels)

with open('FlightPath.czml','w') as tempczml:
	json.dump(flightList,tempczml,indent=4)

# tempczml = open('temp.czml','r')
# flightpathczml = open('FlightPath.czml', "w")
# x = 0
# y = 0
# for line in tempczml:
# 	if re.search("cartographicDegrees", line) and y % 2 == 0:
# 		cartDegree = list() # cartDegree is a list that will contain all the coordinates
# 		# print(flightID[x])
# 		with open(flightdir+"\\"+csvID[x], 'r') as flight_csv:
# 			# flight_reader = csv.reader(flight_csv)
# 			# line_count = 0
# 			# for row in flight_reader:
# 			# 	if line_count == 0:
# 			# 		line_count += 1
# 			# 	else:
# 			# 		cartDegree.append (row[2])
# 			# 		cartDegree.append (row[1])
# 			# 		cartDegree.append (row[3])
# 			# 		line_count += 1
# 			# print(cartDegree) 
# 			# cartDegree is a list of coordinates ('100,200,3000', '110,200,3300') ('x,y,z','x,y,z') 		
# 			cartDegreeString = list(map(float, cartDegree)) 
# 			# print(cartDegreeString) 
# 			# cartDegreeString joins the list of coordinates into 1 string separated by ',' i.e. (100,200,3000,110,200,3300) (x,y,z,x,y,z)
# 			flightpathczml.write("\t\t\t\t\"cartographicDegrees\": [\n" + "\t\t\t\t\t" + cartDegreeString + "\n\t\t\t\t]\n")
# 			x += 1
# 			y += 1
# 			# print(line + "Hey")
# 			lastlocation = len(cartDegree)
# 			#print(cartDegree[lastlocation-3])
# 	elif re.search("cartographicDegrees", line) and y % 2 == 1:
# 		flightpathczml.write("\t\t\t\t\"cartographicDegrees\": [\n" + "\t\t\t\t\t" + cartDegree[lastlocation-3] + ",\n\t\t\t\t\t" + cartDegree[lastlocation-2] + ",\n\t\t\t\t\t"+ cartDegree[lastlocation-1] + "\n\t\t\t\t]\n")
# 		cartDegree.clear() #clear the coordinates list
# 		y +=1
# 	else:
# 		flightpathczml.write(line)	
# 		# print(line)	

# tempczml.close()
# flightpathczml.close()
# os.remove("temp.czml")

# print(Flights)
