#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

def diferenca_tempo(hora1,hora2):
	if(hora1>hora2):
		dif = (hora1.hour - hora2.hour)*60 + hora1.minute - hora2.minute + (hora1.second - hora2.second)/60.0
		return dif
	else:
		dif = (hora2.hour - hora1.hour)*60 + hora2.minute - hora1.minute + (hora2.second - hora1.second)/60.0
		return dif

def millis_para_data(milis, formato):
	milis = float(milis) / 1000.0
	d_ = datetime.datetime.fromtimestamp(milis).strftime(formato)
	d =  datetime.datetime.strptime(d_, formato)
	return d


def tempo_medio_registro_starttime_waze(arquivo_,col_pubmillis,col_startime):
	arquivo = open(arquivo_,'r')
	dif_tempo = 0
	num_tempo = 0
	for linha in arquivo:
		atributos = linha.replace('\n','').split(';')

		data =  millis_para_data(atributos[col_pubmillis],'%Y-%m-%d').date()
		hora =  millis_para_data(atributos[col_pubmillis],'%H:%M:%S').time()
		
		start_data = datetime.datetime.strptime(atributos[col_startime].split(' ')[0], '%Y-%m-%d').date()
		start_hora = datetime.datetime.strptime(atributos[col_startime].split(' ')[1], '%H:%M:%S').time()

		
		if data > datetime.datetime.strptime('2014-01-01', '%Y-%m-%d').date():
			dif_tempo = dif_tempo + (diferenca_tempo(start_hora,hora))
			num_tempo = num_tempo + 1
	print dif_tempo/num_tempo
