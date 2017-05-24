#!/usr/bin/env python
# -*- coding: utf-8 -*-
from acdata import *
from acgeo import *
import os
import datetime
import time
import psycopg2


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
def mescla_acidentes_repetidos_(arquivo_,col_id,col_data_hora,col_usu,col_rua,col_x,col_y):
	#Manter uma lista com os acidentes,uma com os ids dos acidentes repetidos (para que eles nao sejam contados mais de uma vez) e uma com
	#os acidentes apos serem mesclados
	acidentes		= []
	acidentes_temp		= []
	registros_analisados     = [] 
	acidentes_novo		= []

	with open(arquivo_,'r') as arquivo:
		acidentes = arquivo.read().splitlines()
	arquivo.close()
	with open(arquivo_,'r') as arquivo:
		acidentes_temp = arquivo.read().splitlines()
	arquivo.close()
	num_linha 	  = 0
	
	#Parte I: procura os acidentes reportados mais de uma vez
	for registro in acidentes:
		#Armazena os acidentes que casaram para cada rodada
		#Flag pra verificar se o acidente analisado no momento deve ou nao ser inserido em registros_analisados
		acidentes_casados = []
		flag_id_match	  = 0
		atributos = registro.split(';')
		id        = atributos[col_id]
		data	  = atributos[col_data_hora].split(' ')[0]
		usuario	  = atributos[col_usu]
		rua	  = atributos[col_rua]
		x	  = atributos[col_x]
		y	  = atributos[col_y]
		try:		
			acidentes_temp.remove(registro)
		except ValueError:
			pass
		acidentes_casados.append(registro)
		num_linha = num_linha +1
		print num_linha	
		for registro_ in acidentes_temp:
			atributos_ = registro_.split(';')
			id_        = atributos_[col_id]
			data_	   = atributos_[col_data_hora].split(' ')[0]
			usuario_   = atributos_[col_usu]
			rua_	   = atributos_[col_rua]
			x_	   = atributos_[col_x]
			y_	   = atributos_[col_y]
			if id_ not in registros_analisados and id not in registros_analisados and id != id_:
				if data == data_:
					hora      = int(datetime.datetime.strptime(atributos[col_data_hora].split(' ')[1], '%H:%M:%S').strftime("%s"))
					hora_ 	  = int(datetime.datetime.strptime(atributos_[col_data_hora].split(' ')[1],'%H:%M:%S').strftime("%s"))
					#dif_tempo = diferenca_tempo(hora,hora_)
					if (abs(hora-hora_)/60) <= 60.00 :
						distancia = distancia_entre_pontos((x,y),(x_,y_))
						if distancia <= 50.00:
							acidentes_casados.append(registro_)
							acidentes_repetidos.append(id_)
							try:
								acidentes_temp.remove(registro_)
							except ValueError:
								pass
							flag_id_match = 1
		
		#Se o registro analisado nao é repetido, insira-o em acidentes_novo
		if flag_id_match == 1:
			acidentes_repetidos.append(id)
		else:
			acidentes_novo.append(registro)

	print "\nNumeros: "+str(len(acidentes_novos))+','+str(len(acidentes_casados))
	#Parte II:
	saida = open(arquivo_.replace(''),'w')

	for registro_repetido in acidentes_repetidos:
		casados    = []
		for registro_casado in registro_repetido:
			atributos  = registro_casado.replace('\n','').split(';')
			x	   = atributos[col_x]
			y	   = atributos[col_y]
			casados.append((x,y))
		x_centroide,y_centroide = centroide(casados)
		saida.write(';'.join(registro_repetido[0][:col_x])+';'+str(x_centroide)+';'+str(y_centroide)+';'.join(registro_repetido[0][col_y+1:])+str(len(registro_repetido))+'\n')

	for registro_novo in acidentes_novo:
		saida.write(registro_novo.replace('\n','')+'1\n')
	



#Dada um arquivo de acidentes encontra entradas de acidentes notificados mais de uma vez por diferentes usuarios
#Sera considerado o mesmo acidente se: 1) registros com menos de uma hora de diferenca 2)menos de 50m de distancia 
#Manter uma lista com os acidentes,uma com os ids dos acidentes repetidos (para que eles nao sejam contados mais de uma vez) e uma com
#os acidentes apos serem mesclados
def mescla_acidentes_repetidos(arquivo_,col_id,col_data_hora,col_usu,col_rua,col_x,col_y):
	acidentes		= []
	acidentes_temp		= []
	registros_analisados	= []
	acidentes_novo		= []
	numero_linhas		= 0

	#Salva os acidentes do arquivo numa lista e depois a ordena pela data do acidente
	entrada = open(arquivo_,'r') 
	for registro in entrada:
		atributos = registro.replace('\n','').split(';')
		data	  = atributos[col_data_hora].split(' ')[0]
		acidentes_temp.append((data,registro.replace('\n','')))
	entrada.close()
	
	acidentes = list(zip(*sorted(acidentes_temp[:]))[1])

	for registro in acidentes[:]:
		numero_linhas += 1
		print numero_linhas

		atributos = registro.replace('\n','').split(';')
		id        = atributos[col_id]
		data	  = atributos[col_data_hora].split(' ')[0]
		usuario	  = atributos[col_usu]
		rua	  = atributos[col_rua]
		x	  = atributos[col_x]
		y	  = atributos[col_y]

		if id not in registros_analisados:
			registros_analisados.append(id)
			acidentes_novo.append(registro+';'+id)
			acidentes.remove(registro)
		
			
			for registro_ in acidentes[:]:
				atributos_ = registro_.replace('\n','').split(';')
				id_        = atributos_[col_id]
				data_	   = atributos_[col_data_hora].split(' ')[0]
				usuario_   = atributos_[col_usu]
				rua_	   = atributos_[col_rua]
				x_	   = atributos_[col_x]
				y_	   = atributos_[col_y]

				if data < data_:
					break
				if id_ not in registros_analisados:
					if data == data_ and id != id_:
						hora      = int(datetime.datetime.strptime(atributos[col_data_hora].split(' ')[1], '%H:%M:%S').strftime("%s"))
						hora_ 	  = int(datetime.datetime.strptime(atributos_[col_data_hora].split(' ')[1],'%H:%M:%S').strftime("%s"))					
						if (abs(hora-hora_)/60) <= 60.00 :
							distancia = distancia_entre_pontos((x,y),(x_,y_))
							if distancia <= 50.00:
								registros_analisados.append(id_)
								acidentes_novo.append(registro_+';'+id+'\n')
	print "\nNumeros: "+str(len(acidentes_novo))+','+str(len(acidentes))
	#Parte II:
	saida = open(arquivo_.replace('.csv','')+'_saida.csv','w')
	for registro in acidentes_novo:
		saida.write(registro.replace('\n','')+'\n')	

def teste_banco(arquivo_,col_id,col_data_hora,col_usu,col_rua,col_x,col_y):
	entrada_arquivo = open(arquivo_,'r')
	numero_linhas = 0

	try:
    		conn = psycopg2.connect("dbname='waze' user='salatiel' host='localhost' password='thecross'")
		print "Connected to database"
	except:
    		print "I am unable to connect to the database"
	cur = conn.cursor()

	for registro in entrada_arquivo:
		numero_linhas += 1
		print numero_linhas
		atributos = registro.replace('\n','').split(';')
		id        = atributos[col_id]
		data	  = atributos[col_data_hora].split(' ')[0]
		usuario	  = atributos[col_usu]
		rua	  = atributos[col_rua]
		x	  = atributos[col_x]
		y	  = atributos[col_y]
		
		cur.execute("SELECT * from event where date_event ="+"'"+data+"'") #executa query
		rows = cur.fetchall() #armazena o que foi trazido a query
		for r in rows:
			pass
	


			
