# Map the two rides with time slider.  

import gpxpy
import gpxpy.gpx
import folium as folium
from folium import plugins
from datetime import datetime, timedelta
import json



def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

# PARSING FIRST FILE
gpx_file = open('6_20_1.gpx')
gpx = gpxpy.parse(gpx_file)
time = []
# there are two lists for each file because folium polyline needs Lat/lon
# but GeoJSON needs Lon/Lat
points1 = []
points1A = []

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            points1.append([point.longitude, point.latitude])
            points1A.append([point.latitude, point.longitude])
            # convert times
            seconds = (point.time.isoformat())
            t = json.dumps(seconds, default = myconverter)
            #times in weird format, had to get rid of quotes
            t = t.strip('"')
            # fill in list of times
            time.append(t)


# PARSING SECOND FILE
gpx_file = open('6_20_2.gpx')
gpx = gpxpy.parse(gpx_file)
time2 = []
# there are two lists for each file because folium polyline needs Lat/lon
# but GeoJSON needs Lon/Lat
points2 = []
pointsA = []
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            points2.append([point.longitude, point.latitude])
            pointsA.append([point.latitude, point.longitude])
            # convert times
            seconds = (point.time.isoformat())
            t = json.dumps(seconds, default = myconverter)
            #times in weird format, had to get rid of quotes
            t = t.strip('"')
            # fill in list of times
            time2.append(t)

# FOLIUM MAP
# Create Map
# Create map at the first point of the second file
    m = folium.Map(location= pointsA[1], zoom_start=15)
# add lines for each point, but slightly transparent so we can see them both
    folium.vector_layers.PolyLine(pointsA, color="red", weight= 2.5, opacity = .5).add_to(m)
    folium.vector_layers.PolyLine(points1A, color="blue", weight = 2.5, opacity = .5).add_to(m)


###### BEGIN GEOJSON INFORMATION
# GEOJSON allows us to have the time slider and animate the rides
# like a FlyBy on Strava would be animated.

# dividing up points in to smaller groups so that we can have small line segments
#want it to overlap.(currently 1 overlapping element)
def divide_points(list):
    for i in range(0, len(list), 2):
        yield list[i:i+3]

#time and points are in sublists of 3 items each with 1 element of overlap.
newpoints2 = (list(divide_points(points2)))
newtimes2 = (list(divide_points(time2)))
newtimes1 = (list(divide_points(time)))
newpoints1 = (list(divide_points(points1)))

## Create the line segments

lines = []
for i in range(0, len(newpoints1)):
    seg = {'coordinates': newpoints1[i],
    'dates':newtimes1[i],
    'color':'blue'
    }
    lines.append(seg)

for i in range(0, len(newpoints2)):
    seg = {'coordinates': newpoints2[i],
    'dates':newtimes2[i],
    'color':'red'
    }
    lines.append(seg)

#print(lines)


# Features of GeoJSON map overlay
features = [
    {
        'type': 'Feature',
        'geometry': {
            'type': 'LineString',
            'coordinates': line['coordinates'],
        },
        'properties': {
            'times': line['dates'],
            'style': {
                'color': line['color'],
                'weight': line['weight'] if 'weight' in line else 3},
                'icon' : 'circle',
                'fillOpacity': .4,
                'iconstyle':{
                'fillOpacity': .4,
                'stroke-opacity': .4,
                }

        }
    }
    for line in lines
]

#add the TimestampedGeoJson to the Map
geoj = plugins.TimestampedGeoJson({
'type': 'FeatureCollection',
     'features': features,
}, period = 'PT5S'
)

m.add_child(geoj)

# Save map
m.save("map.html")
