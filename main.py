'''
Jenny Melcher and Zeke Mostov
Senior Project Spring 2019
Triathalon Cycling Drafting Detection
This file deals with user input and runs a loop while program is running
to prompt user input
'''

from getDrafting import *
from makeDataFrame import *
from makeMap import *


def main():
	print("Make sure your GPX files are in the current directory \n")

	dfs = getUserFiles()

	dfm = mergeDF(dfs[0],dfs[1])

	#get distance and then get get drafting stats
	dfm = getDisMerge(dfm)
	dfm = getDrafting(dfm)

	segmentarr = getTimeSeg(dfm)
	riderSegments = getRiderOrder(segmentarr[0])

	rider1Behind = riderSegments[3]
	rider2Behind = riderSegments[2]
	#Loop through rider drafting times segments

	getViolation(riderSegments)

	toPrintSegs = input("Would you like to print segments of drafting and rule violation? (y/n): ")
	if toPrintSegs == "y":
		if len(rider1Behind) > 0:
			for i in range (len(rider1Behind)):
				print(
					"The segment of drafting number", i+1, 
					" Rider 1 was drafting Rider 2 they drafted for",
					 rider1Behind[i], "seconds \n"
					)
		if len(rider2Behind) > 0:
			for i in range (len(rider2Behind)):
				print(
					"The segment of drafting number", i+1, 
					" Rider 2 was drafting Rider 1 they drafted for",
					 rider2Behind[i], "seconds \n"
					)
			
	#TODO figure out what info we should return
	#if they where drafting at all?
	#Number of times rider1 was drafting rider2 for at least 15 seconds
	#The duration of each of those segments of drafting
	#Yes/No/Unsure if rider1 broke the rules
	#File Quality


'''
deals with user input
frame manipulations that require tracks and df
prompts users for file names and converts each file
to its own dataframe
then asks the users about additional stats and map
'''
def getUserFiles():
	fileRide1 = input("\n Please enter the name of your first GPX file: ")
	openRide1 = open(fileRide1, 'r')
	parsedGpxFile1 = gpxpy.parse(openRide1)
	track1 = parsedGpxFile1.tracks[0].segments[0].points
	df1 = makeDF(track1)

	fileRide2 = input("\n Please enter the name of your second GPX file: ")
	openRide2 = open(fileRide2, 'r')
	parsedGpxFile2 = gpxpy.parse(openRide2)
	track2 = parsedGpxFile2.tracks[0].segments[0].points
	df2 = makeDF(track2)

	r1q = getQuality(df1)
	r2q = getQuality(df2)
	print("\n Ride 1s", r1q[1])
	print("\n Ride 2s", r2q[1])

	getRideStats = input(
		" \n Would you like to know the total time and distance of each ride? (y/n): "
		)
	#TODO MAKE SURE IT PRINTS OUT CORRECTLY
	if getRideStats == 'y':
		print("\n Ride 1 stats \n")
		df1 = updateDF(track1, df1)
		print("\n Ride 2 stats \n")
		df2 = updateDF(track2, df2)

	toMap = input(
		" \n Would you like to have a map visualization as an html file? called map.html (y/n): "
		)
	if toMap == 'y':
		processAndMakeMap(track1, track2)

	dfs = [df1, df2]

	return dfs

main()
