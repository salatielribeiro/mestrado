#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

#Dadas duas horas, retorna a difetenca entre elas em minutos hora em datetime
def time_difference(time_1,time_2):
	if(time_1>time_2):
		diff = (time_1.hour - time_2.hour)*60 + time_1.minute - time_2.minute + (time_1.second - time_2.second)/60.0
		return diff
	else:
		diff = (time_2.hour - time_1.hour)*60 + time_2.minute - time_1.minute + (time_2.second - time_1.second)/60.0
		return diff

#Dada uma string com uma data (formato YYYY-MM-DD), retorna o dia da semana correspondente a data 
def day_of_week(date_):
	date = datetime.datetime.strptime(date_, '%Y-%m-%d')
	days = ('Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo')
	return days[date.weekday()]

#Dada uma data em milisegundos, retorna a data no formato desejado
def millis_to_date(millis, format):  # @ReservedAssignment
	millis = float(millis) / 1000.0
	d_ = datetime.datetime.fromtimestamp(millis).strftime(format)
	d =  datetime.datetime.strptime(d_, format)
	return d


#Retorna os acidentes separados por mes
def events_by_month(file_,col_date_time):
	file_in = open(file_,'r')
	month_tmp= []
	month	= []
	for row in file_in:
		attributes = row.replace('\n','').split(';')
		date = attributes[col_date_time].split(' ')[0]
		month_day = '-'.join(date.split('-')[:2])
		month.append(month_day)
	for x in set(month):
		month_tmp.append((x,month.count(x)))
	month = sorted(month_tmp)
	return month
	
#Retorna os acidentes separados por dia da semana
def events_by_day_of_week(file_,col_data_hora):
	file_in = open(file_,'r')
	day_week = []
	day_week_count = []
	for row in file_in:
		attributes = row.replace('\n','').split(';')
		date = attributes[col_data_hora].split(' ')[0]
		day  = day_of_week(date)
		day_week.append(day)
	for x in set(day_week):
		day_week_count.append((x,day_week.count(x)))
	return day_week_count

#Retorna os acidentes separados por day (dd/mm/aaaa)
def events_by_day(file_,col_date_time):
	file_in = open(file_,'r')
	day 		= []
	day_tmp 	= []
	for row in file_in:
		attributes = row.replace('\n','').split(';')
		date = attributes[col_date_time].split(' ')[0]
		day.append(date)
	for x in set(day):
		day_tmp.append((x,day.count(x)))
	day = sorted(day_tmp)	
	return day
