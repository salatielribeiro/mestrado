#!/usr/bin/env python
# -*- coding: utf-8 -*-
from acfile import *  # @UnusedWildImport
from acvis import *  # @UnusedWildImport
from acdate import *  # @UnusedWildImport


def main():
	waze_file_path 	= '/home/salatiel/Desktop/dados/belo_horizonte/acidentes/waze/acidentes_belo_horizonte_waze_0716_0517_merged.csv'
	waze_event_file_path = '/home/salatiel/Desktop/dados/belo_horizonte/acidentes/waze/eventos_belo_horizonte_waze_0716_0517.csv'
	#caminho_arquivo_waze_ev	= '/home/salatiel/Desktop/dados/belo_horizonte/acidentes/waze/eventos_belo_horizonte_waze_0716_0517.csv'
	#caminho_arquivo_bhtrans = '/home/salatiel/Desktop/dados/belo_horizonte/acidentes/bh_trans/'
	merge_duplicate_events(waze_event_file_path,0,1,18,9,10,11)
	#vis_events_by_time(waze_file_path)
if __name__ == "__main__":
	main()
