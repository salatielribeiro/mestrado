#!/usr/bin/env python
# -*- coding: utf-8 -*
from geopy.distance import vincenty
from datetime import datetime
import ogr

def distancia_entre_pontos(ponto_1,ponto_2):
	return (vincenty(ponto_1,ponto_2).meters)

def centroide(poly):
	return poly.Centroid()

def create_polygon(coords):          
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for coord in coords:
        ring.AddPoint(coord[0], coord[1])
    #Add first coordinate to close polygon	
    ring.AddPoint(coords[0][0], coords[0][1])

    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    #return poly.ExportToWkt()
    return poly
