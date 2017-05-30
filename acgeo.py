#!/usr/bin/env python
# -*- coding: utf-8 -*
from geopy.distance import vincenty
import ogr

def distance_between_points(point_1,point_2):
	distance = vincenty(point_1,point_2).meters  # @IndentOk
	return distance

def centroid(coords):          
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for coord in coords:
        ring.AddPoint(coord[0], coord[1])
    #Add first coordinate to close polygon	
    ring.AddPoint(coords[0][0], coords[0][1])

    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    #return poly.ExportToWkt()
    return poly.Centroid()
