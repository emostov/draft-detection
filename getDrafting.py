from makeDataFrameV3 import *
import haversine
'''
distance units are in kms from haversine
25 feet is 0.00762
'''

def disformula(lat1, lon1, lat2, lon2):
	#print lat1, lon1, lon2, lat2
	dis = haversine.haversine((lat1,lon1),(lat2,lon2))
	#print dis
	return dis

"""
returns 0 if not within tolerance,
 1 if within tolerance, and 2 if one file does not have cords
"""
def disdraft(lat1, lon1, lat2, lon2):
	#tolerance = 0.00762 #25 feet
	tolerance = 0.01524 #50 feet
	dis = disformula(lat1,lon1,lat2,lon2)

	if dis <= tolerance :
		return 1
	if dis > tolerance:
		return 0
	else:
		return 2

#calculate 2d haversine distance for each row
def getDisMerge(dfmerged):
	dfmerged['dist'] = dfmerged.apply(
		lambda row: disformula(row['lat_x'], row['lon_x'], row['lat_y'], row['lon_y']),
		axis=1)
	return dfmerged

'''
returns 0 if not within tolerance, 1 if within tolerance, 
and 2 if one file does not have cords
applies to all rows
'''
def getDrafting(dfjoined):
	dfjoined['drafting'] = dfjoined.apply(
		lambda row: disdraft(row['lat_x'], row['lon_x'], row['lat_y'], row['lon_y']),
		axis=1)
	return dfjoined

"""
Takes in row of dataframe and the previous row
Outputs what rider is in front in 1 or 2
"""
def compare(row, before):
	
	rider1 = disformula(row.lat_x, row.lon_x, before.lat_x, before.lat_x)
	rider2 = disformula(row.lat_y, row.lat_y, before.lat_x, before.lon_x)

	if rider1 > rider2:
		return 1
	if rider1 < rider2:
		return 2

"""

"""
def getTimeSeg(df):
	timeSegments = []
	segment = []
	before = 0
	segNum = 0
	past = False
	rb = 0
	tupleSeg = []
	infront = []
	for row in df.itertuples():
		if(row.drafting == 0):
			if(before == 1):
				#create time seg and add to array of segs
				s = segment.copy()
				timeSegments.append(s)
				del segment[:]
				t = tupleSeg.copy()
				infront.append(t)
				del tupleSeg[:]
			before = 0
		if(row.drafting == 2):
			if(before == 1):
				#create time seg and add to array of segs
				s = segment.copy()
				timeSegments.append(s)
				del segment[:]
				t = tupleSeg.copy()
				infront.append(t)
				del tupleSeg[:]
			before = 2
		if(row.drafting == 1):
			segment.append(row.seconds)
			before = 1
			if past:
				x = [row.seconds, compare(row, rb)]
				tupleSeg.append(x)
		past = True
		rb = row
	returnarr = [infront, timeSegments]
	return returnarr

def getSigSegs(rider1segs, rider2segs):
	#filter out segments less the 15 seconds
	filteredR1Segs = list(filter(lambda x: len(x) > 15, rider1segs))
	filteredR2Segs = list(filter(lambda x: len(x) > 15, rider2segs))
	returnArr = [filteredR1Segs, filteredR2Segs]
	return [filteredR1Segs, filteredR2Segs]

def getSegLen(segs):
	timeInFront = []
	for seg in segs:
		timeInFront.append(len(seg))
	return timeInFront


'''
	Return an array of arrays
	index 0 segments of seconds that rider 1 was in front
	index 1 segments of seconds that rider 2 was in front
	index 2 number of seconds for each segment rider 1 in front
	index 3 number of seconds for each segment rider 2 in front
'''
def getRiderOrder(infront):
	#returns arrays of when rider 1 is in front and when rider 2 is in front
	rider1segs = [] #segments where rider 1 is in front
	rider2segs = []
	r1seg = [] #for accumulating sub segments
	r2seg = []
	before = 0
	for seg in infront:
		for i in range (len(seg)):
			if seg[i][1] == 1: #rider 1 in front
				if seg[i-1][1] == 2: #end of segment
					x = r2seg.copy()
					rider2segs.append(x)
					del r2seg[:]
				r1seg.append(seg[i][0])
			if seg[i][1] == 2: #rider 2 in front
				if seg[i-1][1] == 1: #end of segment
					x = r1seg.copy()
					rider1segs.append(x)
					del r1seg[:]
				r2seg.append(seg[i][0])

		x = r2seg.copy()
		rider2segs.append(x)
		del r2seg[:]
		y = r1seg.copy()
		rider1segs.append(y)
		del r1seg[:]
	
	filteredSegs = getSigSegs(rider1segs, rider2segs)
	filterR1 = filteredSegs[0]
	filterR2 = filteredSegs[1]
	durationR1 = getSegLen(filterR1) #array of times correlated to segment being drafting
	durationR2 = getSegLen(filterR2)
	#print("rider 1 segments are" , durationR1, '\n')
	#print("rider 2 segments are" , durationR2)
	riderSegments = [filterR1, filterR2, durationR1, durationR2]
	return riderSegments

def getViolation(riderSegments):
	#check quality and if bad determine unsure
	rider1Behind = riderSegments[3]
	rider2Behind = riderSegments[2]
	if len(rider1Behind) > 0:
		r1max = max(rider1Behind)
		if 15 < r1max < 60:
			print("Rider 1 was probably breaking the drafting rule \n")
		if r1max > 60:
			print("Rider 1 was definitley breaking the drafting rule \n")
	else:
		print("Rider 1 was definitley not breaking the drafting rule \n")

	if len(rider2Behind) > 0:
		r2max = max(rider2Behind)
		if 15 < r2max < 60:
			print("Rider 2 was probably breaking the drafting rule \n")
		if r2max > 60:
			print("Rider 2 was definitley breaking the drafting rule \n")
	else:
		print("Rider 2 was definitley not breaking the drafting rule \n")




