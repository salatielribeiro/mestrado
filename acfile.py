#!/usr/bin/env python
# -*- coding: utf-8 -*-
from acdate import *  # @UnusedWildImport
from acgeo import *  # @UnusedWildImport
import os
import datetime  # @Reimport
import time
import psycopg2
import pandas as pd
import numpy as np

#Dado um arquivo csv de eventos, retorna com dataframe com esses dados
def csv_to_dataframe(file_in):
	dtype	={
		"id":str,"datetime_event":object,"date_event":object,"time_event":object,"starttime":object,"endtime":object,"uuid":str,\
	    "country":str,"city":str,"street":str,"lon":float,"lat":float,"type_event":str,"subtype_event":str,"speed":float,"road_type":int,"reliability":int,\
		"confidence":int,"report_by":str,"report_mood":int,"report_rating":int,"in_scale":str,"is_jam_unified_alert":str,"show_facebook_pic":str,\
		"n_comments":int,"n_images":int,"n_thumbs_up":int,"datetime_pubmillis":int,"mgvar":str,"comments":str,"additional_info":object
			}
	df						= pd.read_csv(file_in,sep=';',dtype=dtype)
	df['datetime_event']	= pd.to_datetime(df['datetime_event'])
	df['date_event']		= pd.to_datetime(df['date_event'], format='%Y-%m-%d')
	df['time_event']		= pd.to_datetime(df['time_event'], format='%H:%M:%S').dt.time
	
	if "lon_merged" in df.columns and "lat_merged" in df.columns and "numer_matches" in df.columns:
		df["lon_merged"] 	= pd.to_numeric(df["lon_merged"])	
		df["lat_merged"] 	= pd.to_numeric(df["lat_merged"])	
		df["numer_matches"] = pd.to_numeric(df["numer_matches"])	
	return df

#Dado um arquivo de acidente, coloca-lo no formato adequado. Os primeiros campos sao id,data e hora, data, hora, tipo e subtipo
#Os outros atributos vem em seguida
#Formato data: '%Y-%m-%d %H:%M:%S'
def format_event_file(file_,col_id,col_date_time,header,file_type,erase_file):  # @ReservedAssignment
	file_in 	= open(file_,'r')
	file_out 	= open(file_.replace('.csv','')+'_saida.csv','w')

	if header == True:
		_header_= file_.readline()	

	for row in file_in:
		attributes 		= row.replace('\n','').split(';')
		date_time_temp 	= attributes[col_date_time]
		id 				= attributes [col_id]  # @ReservedAssignment
		row_out			= ''

		if file_type == 'waze':
			try:
				date_time_temp = float(date_time_temp)  # @NoEffect
			except ValueError:
				date_time_temp = 0.0  
			date = millis_to_date(date_time_temp, '%Y-%m-%d').date()	
			time = millis_to_date(date_time_temp, '%H:%M:%S').time()

		elif file_type == 'bhtrans':
			time = date_time_temp.split(' ')[1]
			#Verifica em qual formato a data está
			if '/' in date_time_temp:
				if date_time_temp.split('/')[3]>31: #testar se esta fora do formato YYYY-MM-DD
					date	= date_time_temp.split('/')[2]+'-'+date_time_temp.split('/')[1]+'-'+date_time_temp.split('/')[0]
				else:
					date	= date_time_temp.split('/')[0]+'-'+date_time_temp.split('/')[1]+'-'+date_time_temp.split('/')[2]
			
			elif '-' in date_time_temp:
				if date_time_temp.split('-')[3]>31: #testar se esta fora do formato YYYY-MM-DD
					date	= date_time_temp.split('-')[2]+'-'+date_time_temp.split('-')[1]+'-'+date_time_temp.split('-')[0]
				else:
					date	= date_time_temp
		#Se o arquivo nao for do waze nem da bhtrans, exibe mensagem de erro e sai da funcao
		else:
			print "File not supported!"
			return
		date_time = str(date)+' '+str(time)
		
		if col_id < col_date_time:
			row_out = id+';'+str(date_time)+';'+str(date)+';'+str(time)+';'+';'.join(attributes[:col_id])+';'+';'.join(attributes[col_id+1:col_date_time])+';'+';'.join(attributes[col_date_time:])+'\n'
		else:
			row_out =  id+';'+date_time+';'+date+';'+time+';'+';'.join(attributes[:col_date_time])+';'+';'.join(attributes[col_date_time:col_id])+';'+';'.join(attributes[col_id:])+'\n'
		file_out.write(row_out)

	file_.close()
	if erase_file == True:
		os.remove(file_)
		os.rename(file_.replace('.csv','')+'_saida.csv',file_)

#Dada um arquivo de acidentes e uma categoria, cria um arquivo apenas com essa categoria
def split_type(file_,type_,col_type):
	file_in 	= open(file_,'r')  # @ReservedAssignment
	file_out 	= open(file_.replace('.csv','')+'Tipo.csv','w')

	for row in file_in:
		attributes 	= row.split(';')
		type		= attributes[col_type]  # @ReservedAssignment
		if type == type_:
			file_out.write(row)
	file.close()
	file_out.close()	


#Dada um arquivo de acidentes encontra entradas repetidas
#Nao basta olhar apenas o ID (o usuario pode criar duas contribuicoes com ids diferentes referentes ao mesmo acidentes)
#Sera considerado o mesmo acidente se: 1) registros com menos de uma hora de diferenca 2)menos de 50m de distancia 3)Mesmo usuario 4)Mesma rua
def delete_duplicate_events(file_,col_id,col_date_time,col_user,col_street,col_x,col_y):
	duplicate	= []
	row_number	= 0
	with open(file_,'r') as file_in:  # @ReservedAssignment
		events	= file_in.read().splitlines()
	file_in.close()
	with open(file_,'r') as file_in:  # @ReservedAssignment
		events_tmp = file_in.read().splitlines()
	file_in.close()

	for row in events:
		row_number += 1
		print row_number
		attributes	= row.split(';')
		id			= attributes[col_id]  # @ReservedAssignment
		date	  	= attributes[col_date_time].split(' ')[0]
		user	  	= attributes[col_user]
		sreet	  	= attributes[col_street]
		x	  		= attributes[col_x]
		y	  		= attributes[col_y]

		for row_aux in events_tmp:
			attributes_tmp	= row_aux.split(';')
			id_tmp       	= attributes_tmp[col_id]
			date_tmp     	= attributes_tmp[col_date_time].split(' ')[0]
			user_tmp     	= attributes_tmp[col_user]
			street_tmp   	= attributes_tmp[col_street]
			x_tmp	     	= attributes_tmp[col_x]
			y_tmp	     	= attributes_tmp[col_y]


			if date == date_tmp and user == user_tmp and sreet == street_tmp and id != id_tmp and user != ''  :
				time      		= datetime.datetime.strptime(attributes[col_date_time].split(' ')[1], '%H:%M:%S')
				time_tmp     	= datetime.datetime.strptime(attributes_tmp[col_date_time].split(' ')[1], '%H:%M:%S')
				time_difference_= time_difference(time,time_tmp)
				distance 		= distance_between_points((x,y),(x_tmp,y_tmp))
				if sorted((id,id_tmp)) not in duplicate and time_difference_ <= 30.0 and distance <=50.0:
					duplicate.append(sorted((id,id_tmp)))
	return duplicate

#Dado um arquivo e os ids dos registros a serem excluidos, cria um novo arquivo sem esses registros e exclui o antigo
def delete_entries(file_,id_list,col_id):
	file_in  =	open(file_,'r')  # @ReservedAssignment
	file_out =	open(file_.replace('.csv','')+'_saida.csv','w')
	
	for linha in file_in:
		atributos 	= linha.split(';')
		id 			= atributos[col_id]  # @ReservedAssignment
		match_id 	= 0
		for id_ in id_list:		
			if id == id_[0]:
				match_id = 1
				break
		if match_id == 0:
			file_out.write(linha)

	file_in.close()
	file_out.close()
	os.remove(file_)
	os.rename(file_.replace('.csv','')+'_saida.csv',file_)

#Dada um file_in de acidentes encontra entradas de acidentes notificados mais de uma vez por diferentes usuarios
#Sera considerado o mesmo acidente se: 1) registros com menos de uma hora de diferenca 2)menos de 50m de distancia 
#Manter uma lista com os acidentes,uma com os ids dos acidentes repetidos (para que eles nao sejam contados mais de uma vez) e uma com
#os acidentes apos serem mesclados
def merge_duplicate_events(file_,col_id,col_date_time,col_user,col_street,col_x,col_y):
	file_in 		= open(file_,'r')
	file_out   		= open(file_.replace('.csv','_merged.csv'),'w')
	credentials 	= open("credentials_db",'r').readline().strip().split(',')
	processed_rows 	= []
	row_number 		= 0
	header  		= file_in.readline().strip()
	file_out.write(header+";lon_merged;lat_merged;number_matches\n")

	try:
		conn = psycopg2.connect("dbname='"+credentials[0]+"' user='"+credentials[1]+"' host='"+credentials[2]+"' password='"+credentials[3]+"'")
		print "Connected to database"
	except:
		print "I am unable to connect to the database"
	cur = conn.cursor()
	
	for row_file in file_in:
		number_matches  		= 0
		rows 					= []
		same_event 				= []
		same_event_coordinates	= []
		row_number 				+= 1
		print row_number

		attributes	= row_file.replace('\n','').split(';')
		id        	= attributes[col_id]  # @ReservedAssignment
		data	  	= attributes[col_date_time].split(' ')[0]
		time      	= datetime.datetime.strptime(attributes[col_date_time], '%Y-%m-%d %H:%M:%S')
		user	  	= attributes[col_user]  # @UnusedVariable
		street	  	= attributes[col_street]  # @UnusedVariable
		x	  		= attributes[col_x]
		y	  		= attributes[col_y]
	
		if id not in processed_rows and id != ' ' and data!=' ':

			same_event_coordinates.append([float(x),float(y)])
			same_event.append([time,';'.join(attributes)])
			processed_rows.append(id)

			cur.execute("SELECT * from event where date_event ="+"'"+data+"'"+"and id!="+"'"+id+"'" ) #executa query
			rows = cur.fetchall() #armazena o que foi trazido a query
	
			for row_db in rows:
				id_        		= row_db[col_id]
				date_	   		= row_db[col_date_time].strftime('%Y-%m-%d') #Recupera do banco como datetime, aqui converto pra string no formato certo @UnusedVariable
				time_ 	   		= row_db[col_date_time]
				user_			= row_db[col_user]  # @UnusedVariable
				street_	   		= row_db[col_street]  # @UnusedVariable
				x_	   			= row_db[col_x]
				y_	   			= row_db[col_y]

				time_difference_= time_difference(time,time_)
				
				if time_difference_ <= 60.00:
					distance = distance_between_points((x,y),(x_,y_))
					
					if distance <= 50.00:
						row_ 			= ['' if attribute == None else str(attribute) for attribute in list(row_db)]
						number_matches +=1
						same_event_row 	= ';'.join(row_)
						same_event_coordinates.append((float(x_),float(y_)))
						same_event.append([time_,same_event_row])
						processed_rows.append(id_)

			if len(same_event)>1:
				mean_coordinate  	= np.mean(same_event_coordinates,axis=0)
				new_event_row 		= str(sorted(same_event)[1][1])+";"+str(mean_coordinate[0])+";"+str(mean_coordinate[1])+";"+str(number_matches)+"\n"
				file_out.write(new_event_row)
			else:
				file_out.write(';'.join(attributes)+";0.0;0.0;"+str(number_matches)+"\n")
