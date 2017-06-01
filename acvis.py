#!/usr/bin/env python
# -*- coding: utf-8 -*-
from acdate import *  # @UnusedWildImport
import matplotlib.pyplot as plt
import pandas as pd  # @UnusedImport
from acfile import *  # @UnusedWildImport

def vis_precipitation():
	pass
def vis_accident_event():
	pass
def vis_events_by_day(file_,colt_date_time):
	day 			= zip(*events_by_day(file_,colt_date_time))[0]
	day 			= [pd.to_datetime(d,format='%Y-%m-%d') for d in day]
	number_of_days 	= zip(*events_by_day(file_,colt_date_time))[1]
	plt.plot(day,number_of_days, c='darkgreen', alpha=0.8,marker='s',markersize=5,label = "Dia")
	plt.show()

def vis_events_by_time(file_):
	file_in 		= open(file_,'r')
	df 				= csv_to_dataframe(file_in)
	df["time_event"]= df["time_event"].map(lambda t: datetime.datetime.strptime(t.strftime('%H:00'), '%H:00'))
	#time_count = time.value_counts().sort_index()
	
	accident_minor 			= df.loc[df['subtype_event'] == "ACCIDENT_MINOR"]
	accident_major 			= df.loc[df['subtype_event'] == "ACCIDENT_MAJOR"]
	time_by_accident_major 	= accident_major['time_event'].map(lambda t: datetime.datetime.strptime(t.strftime('%H:00'), '%H:00')).value_counts().sort_index()
	time_by_accident_minor 	= accident_minor['time_event'].map(lambda t: datetime.datetime.strptime(t.strftime('%H:00'), '%H:00')).value_counts().sort_index()
	number_matches_count 	= df["number_matches"].value_counts().sort_index()
	ax = plt.gca() 
	#ax.grid(which='both',alpha=0.5)
	#plt.xticks(rotation='45',fontsize=11)
	#plt.plot(accident_minor['subtype_event'].index.tolist(),accident_minor['subtype_event'])
	#plt.ylabel('Number of accidents')
	#plt.xlabel('Hour')
	#plt.plot(time_count.index.tolist(),time_count)
	#plt.plot(time_by_accident_minor.index.tolist(),time_by_accident_minor)
	#plt.plot(time_by_accident_major.index.tolist(),time_by_accident_major)]
	plt.plot(number_matches_count.index.tolist(),number_matches_count)
	plt.show()
	
def vis_events_by_day_of_week(file_,col_date_time):
	pass
def vis_events(file_,col_date_time):
	pass


