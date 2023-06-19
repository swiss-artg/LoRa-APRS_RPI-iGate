#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Python Modul Config.py
Enthält alle Globalen Variablen
"""

import configparser
import os
import pdb
import logging
import re
import datetime


__version__     = "0.0.3"
__author__      = "HB9PAE, Peter"
__copyright__   = "Copyright 2023"
__email__       = "hb9pae@gmail.com"

Version = __version__
myConfig = "/home/hb9pae/RPI-iGate-LoRa/igate.ini"

Frequ   = 433775000
SR      = 12

StartTime = datetime.datetime.now()
DisplayTimeout = 60

Temperature = 1.0
AirPressureNN = 1.0
Humidity = 1.0

LastMsg = "--- None ---"
RxCount = 0
PktErr = 0
PktSent = 0

LastPktRRSI = 0
CurrtRRSI = 0
SNR = 0


# Test auf ungültige Zeichen
def match(strg, search=re.compile(r'[^A-Z0-9.-]').search):
	res = bool(search(strg))
	return(True)

# Umrechnen von Dezimal-Grad zu Grad-Minuten
def grad2min(_lat, _lon) :
	_lonGrad = int(abs(_lon))
	_lonMin = 60.0 * (_lon - _lonGrad)
	lonstr = f"{_lonGrad:d}{_lonMin:.2f}"
	if (_lon > 0) :
		lonstr = lonstr.zfill(8) + "E"
	else :
		lonstr = lonstr + "W"
	_latGrad = int(abs(_lat))
	_latMin = 60* (_lat - _latGrad)
	latstr = f"{_latGrad:d}{_latMin:.2f}"
	if (_lat > 0) :
		latstr = latstr.zfill(7) + "N"
	else :
		latstr = latstr + "S"
	return(latstr, lonstr)

def setGlobals(_conf) :
	global POS

	#pdb.set_trace()
	for section in _conf :
		for key in _conf[section] :
			globals()[key.upper()] = _conf[section][key]
		POS = grad2min(float(LON), float(LAT) )


def getConfig(file) :
	if (os.path.isfile(file)) :
		config = configparser.ConfigParser()
		config.read(file)
		dictionary = {}
		for section in config.sections():
			dictionary[section] = {}
			for option in config.options(section):
				dictionary[section][option] = config.get(section, option)
		return(dictionary)
	else :
		mkConfig(file)
		exit(1)

def mkConfig(file) :
		logging.warning("No Configfile found, create new one and exit Program")

		# ---- Write Header to  Configfile 
		now = datetime.datetime.now() 
		header1 = "# APRS iGate configuration\n"
		header2 = "# (c) hb9pae@gmail.com\n"
		header3 = now.strftime("# Created: %d/%m/%Y %H:%M:%S\n")
		f = open(file, "w")
		f.writelines(header1)
		f.writelines(header2)
		f.writelines(header3)
		f.close()

		# ---- Write Configuration Template 
		_conf=configparser.ConfigParser()
		_conf["APRS-IS"] = {
			"Call": "NOCALL", "Passcode" : "123456", "Info" : "LoRa iGate", "Aprsis" : "False",\
			"lon" : "47.53668", "lat" : "8.58164", "height" : "399",\
			"beaconinterval" : "300", "BeaconMessage" : "-", "BME280" : "True", "WxInterval" : "300"\
			}
		with open(file, 'a') as configfile:
			_conf.write(configfile)
		

def main() :
	myconf = getConfig("test.ini")
	setGlobals(myconf)


if __name__ == "__main__":
        main()




