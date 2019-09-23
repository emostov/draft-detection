"""
Dataframe operations up until they are merged
"""
import gpxpy
import datetime
from geopy import distance
from math import sqrt, floor
import pandas as pd
import haversine
from datetime import datetime,timedelta


#takes a track as input and returns a data frame with time
def makeDF(track):
	dataFrame = pd.DataFrame(columns=['seconds','lon','lat','alt','time'])
	for point in track:
		sec = secondsTime(point.time)
		dataFrame = dataFrame.append(
			{'seconds' : sec, 'lon': point.longitude, 'lat' : point.latitude, 'alt' : point.elevation, 'time' : point.time},
			ignore_index=True)
		
	return dataFrame

"""
takes 2 dataframes and merges them on seconds collum
"""
def mergeDF(dfa, dfb):
	dfmerged = pd.merge(dfa, dfb, on='seconds', how='outer')
	return dfmerged


#update data frome with haversine 2dimensional
#and 3dimensional distances
def updateDF(track, df):
	alt_dif = [0]
	time_dif = [0]
	
	dist_hav = [0]
	
	dist_hav_no_alt = [0]
	dist_dif_hav_2d = [0]

	for index in range(len(track)):
		if index == 0:
			pass
		else:
			start = track[index-1]
			stop = track[index]
			distance_hav_2d = haversine.haversine((start.latitude, start.longitude), (stop.latitude, stop.longitude))*1000
			dist_dif_hav_2d.append(distance_hav_2d)
			dist_hav_no_alt.append(dist_hav_no_alt[-1] + distance_hav_2d)
			alt_d = start.elevation - stop.elevation
			alt_dif.append(alt_d)
			distance_hav_3d = sqrt(distance_hav_2d**2 + (alt_d)**2)
			time_delta = (stop.time - start.time).total_seconds()
			time_dif.append(time_delta)
			dist_hav.append(dist_hav[-1] + distance_hav_3d) 
	df['dist_hav_2d'] = dist_hav_no_alt
	df['dis_hav_3d'] = dist_hav
	df['alt_dif'] = alt_dif
	df['time_dif'] = time_dif
	df['dis_dif_hav_2d'] = dist_dif_hav_2d

	print('Haversine 2D : ', dist_hav_no_alt[-1], 'meters')
	print('Haversine 3D : ', dist_hav[-1], 'meters')
	print('Total Time : ', floor(sum(time_dif)/60),' min ', int(sum(time_dif)%60),' sec ')

	return df


'''
seconds time takes in a datetime and puts out conversion to seconds since 1/1/1970
'''
def secondsTime(dt):
	dateN = datetime(1970, 1, 1)
	dateN.replace(tzinfo=None)
	d = dt.replace(tzinfo=None)
	delta = d - dateN
	seconds = delta.seconds
	return seconds

'''
checks a data frame of indivdual ride to see if data points are missing
if more then 2% of data points are missing relative to elapsed time
the ride is determined to be poor quality
'''

def getQuality(df):
	missing = 0
	rideSize = len(df.index)
	before = 0
	for row in df.itertuples():
		if before != 0:
			if row.seconds > (before.seconds + 1):
				missing = missing + 1
		before = row

	qualityInt = missing/rideSize
	#print("Missing, Ridesize, qualityint:", missing, rideSize, qualityInt)
	if qualityInt >.01:
		quality = "file is not good enough quality to have confidence in determinig drafting \n"
	else:
		quality = "file quality is good \n"

	return [qualityInt, quality]










