#!/usr/bin/env python
# -*- coding: utf-8 -*-
from acdata import *
from acgeo import *
import os
import datetime


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
			try:
				data_hora_temp == float(data_hora_temp)
			except ValueError:
   				data_hora_temp = 0.0
			data = millis_para_data(data_hora_temp, '%Y-%m-%d').date()	
			hora = millis_para_data(data_hora_temp, '%H:%M:%S').time()

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

#Dada um arquivo de acidentes e uma categoria, cria um arquivo apenas com essa categoria
def separa_tipo(arquivo_,tipo_,col_tipo):
	arquivo = open(arquivo_,'r')
	saida 	= open(arquivo_.replace('.csv','')+'Tipo.csv','w')

	for linha in arquivo:
		atributos = linha.split(';')
		tipo	  = atributos[col_tipo]
		if tipo == tipo_:
			saida.write(linha)
	arquivo.close()
	saida.close()	


#Dada um arquivo de acidentes encontra entradas repetidas
#Nao basta olhar apenas o ID (o usuario pode criar duas contribuicoes com ids diferentes referentes ao mesmo acidentes)
#Sera considerado o mesmo acidente se: 1) registros com menos de uma hora de diferenca 2)menos de 50m de distancia 3)Mesmo usuario 4)Mesma rua
def entradas_repetidas(arquivo_,col_id,col_data_hora,col_usu,col_rua,col_x,col_y):
	repetidos     = []
	acidentes	= []
	acidentes_aux   = []
	num_linha = 0
	with open(arquivo_,'r') as arquivo:
		acidentes = arquivo.read().splitlines()
	arquivo.close()
	with open(arquivo_,'r') as arquivo:
		acidentes_aux = arquivo.read().splitlines()
	arquivo.close()

	for linha in acidentes:
		num_linha = num_linha + 1
		print num_linha
		atributos = linha.split(';')
		id        = atributos[col_id]
		data	  = atributos[col_data_hora].split(' ')[0]
		usuario	  = atributos[col_usu]
		rua	  = atributos[col_rua]
		x	  = atributos[col_x]
		y	  = atributos[col_y]

		for linha_aux in acidentes_aux:
			atributos_aux = linha_aux.split(';')
			id_aux       = atributos_aux[col_id]
			data_aux     = atributos_aux[col_data_hora].split(' ')[0]
			usuario_aux  = atributos_aux[col_usu]
			rua_aux      = atributos_aux[col_rua]
			x_aux	     = atributos_aux[col_x]
			y_aux	     = atributos_aux[col_y]


			if data == data_aux and usuario == usuario_aux and rua == rua_aux and id != id_aux and usuario != ''  :
				hora      	= datetime.datetime.strptime(atributos[col_data_hora].split(' ')[1], '%H:%M:%S')
				hora_aux     	= datetime.datetime.strptime(atributos_aux[col_data_hora].split(' ')[1], '%H:%M:%S')
				dif_tempo 		= diferenca_tempo(hora,hora_aux)
				distancia 	= distancia_entre_pontos((x,y),(x_aux,y_aux))
				if sorted((id,id_aux)) not in repetidos and dif_tempo <= 30.0 and distancia <=50.0:
					repetidos.append(sorted((id,id_aux)))
	return repetidos

#Dado um arquivo e os ids dos registros a serem excluidos, cria um novo arquivo sem esses registros e exclui o antigo
def exclui_registros(arquivo_,id_lista,col_id):
	arquivo       =	open(arquivo_,'r')
	arquivo_saida = open(arquivo_.replace('.csv','')+'_saida.csv','w')
	
	for linha in arquivo:
		atributos = linha.split(';')
		id = atributos[col_id]
		match_id = 0
		for id_ in id_lista:		
			if id == id_[0]:
				match_id = 1
				break
		if match_id == 0:
			arquivo_saida.write(linha)

	arquivo.close()
	arquivo_saida.close()
	os.remove(arquivo_)
	os.rename(arquivo_.replace('.csv','')+'_saida.csv',arquivo_)


#Dada um arquivo de acidentes encontra entradas de acidentes notificados mais de uma vez por diferentes usuarios
#Sera considerado o mesmo acidente se: 1) registros com menos de uma hora de diferenca 2)menos de 50m de distancia 
def mescla_acidentes_repetidos(arquivo_,col_id,col_data_hora,col_usu,col_rua,col_x,col_y):
	repetidos     = []
	acidentes	= []
	acidentes_aux   = []
	num_linha = 0
	with open(arquivo_,'r') as arquivo:
		acidentes = arquivo.read().splitlines()
	arquivo.close()
	with open(arquivo_,'r') as arquivo:
		acidentes_aux = arquivo.read().splitlines()
	arquivo.close()

	for entrada in acidentes:
		


