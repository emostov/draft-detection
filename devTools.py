from getDrafting import *
from makeDataFrame import *
from main import *
from makeMap import *

def mainDev():
	bothdf = openAndMakeDF3()
	dfmerge = mergeDF(bothdf[0], bothdf[1])

	dfmerge = getDisMerge(dfmerge)
	dfmerge = getDrafting(dfmerge)

	segmentarr = getTimeSeg(dfmerge)
	riderSegments = getRiderOrder(segmentarr[0])
	rider1Behind = riderSegments[3]
	rider2Behind = riderSegments[2]
	#Loop through rider drafting times segments

	getViolation(riderSegments)
	
	if len(rider1Behind) > 0:
		for i in range (len(rider1Behind)):
			print(
				"The", i+1, 
				" time Rider 1 was drafting Rider 2 they drafted for",
				 rider1Behind[i], "seconds \n"
				)
	if len(rider2Behind) > 0:
		for i in range (len(rider2Behind)):
			print(
				"The", i+1, 
				" time Rider 2 was drafting Rider 1 they drafted for",
				 rider2Behind[i], "seconds \n"
				)

	#print (dfmerge)

#hardcode in names for convience testing
def openmain():
	openGpxFile = open('6_20_1.gpx', 'r')
	parsedGpxFile = gpxpy.parse(openGpxFile)
	track1 = parsedGpxFile.tracks[0].segments[0].points

	openGpxFile = open('6_20_2.gpx', 'r')
	parsedGpxFile = gpxpy.parse(openGpxFile)
	track2 = parsedGpxFile.tracks[0].segments[0].points

	return [track1, track2]

#for opening hardcoded data frames
def openAndMakeDF3():
	#ask use for files and get tracks
	tracks = openmain()
	track1 = tracks[0]
	track2 = tracks[1]
	processAndMakeMap(track1, track2)

	#put tracks into data frames
	dataFrame1 = makeDF(track1)
	dataFrame2 = makeDF(track2)

	r1q = getQuality(dataFrame1)
	r2q = getQuality(dataFrame2)
	print("Ride 1s", r1q[1])
	print("Ride 2s", r2q[1])


	#update data frames
	#dataFrame1 = updateDF(track1, dataFrame1)
	#dataFrame2 = updateDF(track2, dataFrame2)

	bothDataFrames = [dataFrame1, dataFrame2]
	return bothDataFrames

mainDev()