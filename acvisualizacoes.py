#!/usr/bin/env python
# -*- coding: utf-8 -*-
from acdata import *
import matplotlib.pyplot as plt
import pandas as pd

def vis_precipitacoes():
	pass
def vis_acidentes_evento():
	pass
def vis_acidentes_dia(arquivo_,col_data_hora):
	dia 	= zip(*acidentes_dia(arquivo_,col_data_hora))[0]
	dia 	= [pd.to_datetime(d,format='%Y-%m-%d') for d in dia]
  	qt_dia 	= zip(*acidentes_dia(arquivo_,col_data_hora))[1]
	plt.plot(dia,qt_dia, c='darkgreen', alpha=0.8,marker='s',markersize=5,label = "Dia")
	plt.show()

def vis_acidentes_dia_hora(arquivo_,col_data_hora):
	pass
def vis_acidentes_dia_semana(arquivo_,col_data_hora):
	pass
def vis_acidentes_mes(arquivo_,col_data_hora):
	pass

