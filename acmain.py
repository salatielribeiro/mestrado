#!/usr/bin/env python
# -*- coding: utf-8 -*-
from acarquivo import *
from acvisualizacoes import *

def main():
	caminho_arquivo_waze 	= '/home/salatiel/Desktop/dados/belo_horizonte/acidentes/waze/acidentes_belo_horizonte_waze_0716_0517.csv'
	caminho_arquivo_bhtrans = '/home/salatiel/Desktop/dados/belo_horizonte/acidentes/bh_trans/'
	#formata_arquivo_acidente(arquivo=caminho_arquivo_waze,col_id=2,col_data_hora=24,cabecalho=False,tipo_arquivo='waze',apagar=False)
	#tempo_medio_registro_starttime_waze(arquivo_=caminho_arquivo_waze,col_pubmillis=27, col_startime=4)
	#acidentes_mes(caminho_arquivo_waze,4)
	#acidentes_dia_semana(caminho_arquivo_waze,1)
	vis_acidentes_dia(caminho_arquivo_waze,1)
if __name__ == "__main__":
    main()
