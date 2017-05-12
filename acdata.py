#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

def millis_para_data(milis, formato):
	milis = float(milis) / 1000.0
	return datetime.datetime.fromtimestamp(milis).strftime(formato)
