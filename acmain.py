#!/usr/bin/env python
# -*- coding: utf-8 -*-
from acarquivo import *

def main():
	caminho_arquivo_waze 	= '/home/salatiel/Desktop/dados/belo_horizonte/acidentes/waze/acidente_bh_waze_0616_0317.csv'
	caminho_arquivo_bhtrans = '/home/salatiel/Desktop/dados/belo_horizonte/acidentes/bh_trans/'
	#formata_arquivo_acidente(arquivo=caminho_arquivo_waze,col_id=2,col_data_hora=24,cabecalho=False,tipo_arquivo='waze',apagar=False)
	tempo_medio_registro_starttime_waze(arquivo_=caminho_arquivo_waze,col_pubmillis=27, col_startime=4)
if __name__ == "__main__":
    main()
