#!/usr/bin/env python
# -*- coding: utf-8 -*-
from acdata import *  # @UnusedWildImport
import matplotlib.pyplot as plt
import pandas as pd

def vis_precipitation():
	pass
def vis_accident_event():
	pass
def vis_events_by_day(file_,colt_date_time):
	day 	= zip(*events_by_day(file_,colt_date_time))[0]
	day 	= [pd.to_datetime(d,format='%Y-%m-%d') for d in day]
	number_of_days 	= zip(*events_by_day(file_,colt_date_time))[1]
	plt.plot(day,number_of_days, c='darkgreen', alpha=0.8,marker='s',markersize=5,label = "Dia")
	plt.show()

def vis_events_by_time(file_,col_date_time):
	pass
def vis_events_by_day_of_week(file_,col_date_time):
	pass
def vis_events(file_,col_date_time):
	pass
