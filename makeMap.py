#!/usr/bin/python
# -*- coding: utf-8 -*-

import folium as folium
from folium import plugins
from datetime import datetime
import json


# runs tracks through processing and then passes them off to setupMap

def processAndMakeMap(track1, track2):
    processed1 = processTrack(track1)
    processed2 = processTrack(track2)
    setupMap(processed1, processed2)


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def divide_points(list):
    for i in range(0, len(list), 2):
        yield list[i:i + 3]

# takes track and outputs time, points and pointsA in an array

def processTrack(track):
    time = []

    # there are two lists for each file because folium polyline needs Lat/lon
    # but GeoJSON needs Lon/Lat

    points1 = []
    points1A = []
    for point in track:
        points1.append([point.longitude, point.latitude])
        points1A.append([point.latitude, point.longitude])

        # convert times

        seconds = point.time.isoformat()
        t = json.dumps(seconds, default=myconverter)

        # times in weird format, had to get rid of quotes

        t = t.strip('"')

        # fill in list of times

        time.append(t)

    return [time, points1, points1A]


# takes proceessed track and outputs an html map that animates rides

def setupMap(processed1, processed2):
    points1 = processed1[1]
    points1A = processed1[2]
    time1 = processed1[0]

    points2 = processed2[1]
    points2A = processed2[2]
    time2 = processed2[0]

    # Create map at the first point of the second file

    m = folium.Map(location=points2A[1], zoom_start=15)

    # add lines for each point, but slightly transparent so we can see them both

    folium.vector_layers.PolyLine(points2A, color='red', weight=2.5,
                                  opacity=.5).add_to(m)

    folium.vector_layers.PolyLine(points1A, color='blue', weight=2.5,
                                  opacity=.5).add_to(m)

    # time and points are in sublists of 3 items each with 1 element of overlap.

    newpoints2 = list(divide_points(points2))
    newtimes2 = list(divide_points(time2))
    newtimes1 = list(divide_points(time1))
    newpoints1 = list(divide_points(points1))

    # # Create the line segments

    lines = []
    for i in range(0, len(newpoints1)):
        seg = {'coordinates': newpoints1[i], 'dates': newtimes1[i],
               'color': 'blue'}
        lines.append(seg)

    for i in range(0, len(newpoints2)):
        seg = {'coordinates': newpoints2[i], 'dates': newtimes2[i],
               'color': 'red'}
        lines.append(seg)

    # print(lines)

    # Features of GeoJSON map overlay

    features = [{'type': 'Feature', 'geometry': {'type': 'LineString',
                'coordinates': line['coordinates']}, 'properties': {
        'times': line['dates'],
        'style': {'color': line['color'], 'weight': (line['weight'
                  ] if 'weight' in line else 3)},
        'icon': 'circle',
        'fillOpacity': .4,
        'iconstyle': {'radius': 2, 'fillOpacity': .4, 'stroke-opacity': .2},
        }} for line in lines]

    # add the TimestampedGeoJson to the Map

    geoj = plugins.TimestampedGeoJson({'type': 'FeatureCollection',
            'features': features}, period='PT5S')

    m.add_child(geoj)

    # Save map

    m.save('map.html')

