import csv

outputFile = open('testczml.czml','a')
i = 0
with open('data.csv','r') as inputFile:
	inputFileReader = csv.reader(inputFile)
	for row in inputFileReader:
		outputFile.write(row[0] + "," + row[3] + "," + row[1] + "," + row[2] + ",")
		outputFile.write('\n')

