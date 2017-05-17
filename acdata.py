#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

#Dadas duas horas, retorna a difetenca entre elas em minutos
def diferenca_tempo(hora1,hora2):
	if(hora1>hora2):
		dif = (hora1.hour - hora2.hour)*60 + hora1.minute - hora2.minute + (hora1.second - hora2.second)/60.0
		return dif
	else:
		dif = (hora2.hour - hora1.hour)*60 + hora2.minute - hora1.minute + (hora2.second - hora1.second)/60.0
		return dif

#Dada uma string com uma data (formato YYYY-MM-DD), retorna o dia da semana correspondente a data 
def dia_semana(data_):
	data = datetime.datetime.strptime(data_, '%Y-%m-%d')
	dias = ('Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo')
	return dias[data.weekday()]

#Dada uma data em milisegundos, retorna a data no formato desejado
def millis_para_data(milis, formato):
	milis = float(milis) / 1000.0
	d_ = datetime.datetime.fromtimestamp(milis).strftime(formato)
	d =  datetime.datetime.strptime(d_, formato)
	return d


#Conta a diferenca media entre o horario de registro de acidente e o contador de notificao (starttime)
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

#Retorna os acidentes separados por mes
def acidentes_mes(arquivo_,col_data_hora):
	arquivo = open(arquivo_,'r')
	mes_temp= []
	mes	= []
	cont_mes= []
	for linha in arquivo:
		atributos = linha.replace('\n','').split(';')
		data = atributos[col_data_hora].split(' ')[0]
		mes_dia = '-'.join(data.split('-')[:2])
		mes.append(mes_dia)
	for x in set(mes):
		mes_temp.append((x,mes.count(x)))
	mes = sorted(mes_temp)
	return mes
	
#Retorna os acidentes separados por dia da semana
def acidentes_dia_semana(arquivo_,col_data_hora):
	arquivo = open(arquivo_,'r')
	dia_semana_ = []
	cont_dia_semana = []
	for linha in arquivo:
		atributos = linha.replace('\n','').split(';')
		data = atributos[col_data_hora].split(' ')[0]
		dia  = dia_semana(data)
		dia_semana_.append(dia)
	for x in set(dia_semana_):
		cont_dia_semana.append((x,dia_semana_.count(x)))
	return cont_dia_semana

#Retorna os acidentes separados por dia (dd/mm/aaaa)
def acidentes_dia(arquivo_,col_data_hora):
	arquivo = open(arquivo_,'r')
	dia 		= []
	dia_temp 	= []
	for linha in arquivo:
		atributos = linha.replace('\n','').split(';')
		data = atributos[col_data_hora].split(' ')[0]
		dia.append(data)
	for x in set(dia):
		dia_temp.append((x,dia.count(x)))
	dia = sorted(dia_temp)	
	return dia
