#!/usr/bin/env python
# -*- coding: utf-8 -*-
from acdata import *
import os


#Dado um arquivo de acidente, coloca-lo no formato adequado. Os primeiros campos sao id,data e hora, data, hora, tipo e subtipo
#Os outros atributos vem em seguida
#Formato data: '%Y-%m-%d %H:%M:%S'
def formata_arquivo_acidente(arquivo,col_id,col_data_hora,cabecalho,tipo_arquivo,apagar):
	arquivo_ = open(arquivo,'r')
	arquivo_saida = open(arquivo.replace('.csv','')+'_saida.csv','w')

	if cabecalho == True:
		cabecalho_ = arquivo_.readline()	

	for linha in arquivo_:
		atributos 	= linha.replace('\n','').split(';')
		data_hora_temp 	= atributos[col_data_hora]
		id = atributos [col_id]
		linha_saida	= ''

		if tipo_arquivo == 'waze':
			data = millis_para_data(float(data_hora_temp), '%Y-%m-%d').date()	
			hora = millis_para_data(float(data_hora_temp), '%H:%M:%S').time()

		elif tipo_arquivo == 'bhtrans':
			hora = data_hora_temp.split(' ')[1]
			#Verifica em qual formato a data está
			if '/' in data_hora_temp:
				if data_hora_temp.split('/')[3]>31: #testar se esta fora do formato YYYY-MM-DD
					data=data_hora_temp.split('/')[2]+'-'+data_hora_temp.split('/')[1]+'-'+data_hora_temp.split('/')[0]
				else:
					data=data_hora_temp.split('/')[0]+'-'+data_hora_temp.split('/')[1]+'-'+data_hora_temp.split('/')[2]
			
			elif '-' in data_hora_temp:
				if data_hora_temp.split('-')[3]>31: #testar se esta fora do formato YYYY-MM-DD
					data=data_hora_temp.split('-')[2]+'-'+data_hora_temp.split('-')[1]+'-'+data_hora_temp.split('-')[0]
				else:
					data = data_hora_temp
		#Se o arquivo nao for do waze nem da bhtrans, exibe mensagem de erro e sai da funcao
		else:
			print "Tipo de arquivo nao suportado!"
			return
		data_hora = str(data)+' '+str(hora)
		
		if col_id < col_data_hora:
			linha_saida = id+';'+str(data_hora)+';'+str(data)+';'+str(hora)+';'+';'.join(atributos[:col_id])+';'+';'.join(atributos[col_id+1:col_data_hora])+';'+';'.join(atributos[col_data_hora:])+'\n'
		else:
			linha_saida =  id+';'+data_hora+';'+data+';'+hora+';'+';'.join(atributos[:col_data_hora])+';'+';'.join(atributos[col_data_hora:col_id])+';'+';'.join(atributos[col_id:])+'\n'
		arquivo_saida.write(linha_saida)

	arquivo_.close()
	if apagar == True:
		os.remove(arquivo)
		os.rename(arquivo.replace('.csv','')+'_saida.csv',arquivo)
