#!/usr/bin/env python
# -*- coding: utf-8 -*
from geopy.distance import vincenty
from datetime import datetime

def distancia_entre_pontos(ponto_1,ponto_2):
	return (vincenty(ponto_1,ponto_2).meters)
