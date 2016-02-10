#!/usr/bin/python

import ConfigParser
import logging
import json
import os

def stringifyJSON(data):
	return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


def getJSONData(filepath):
	f = open(filepath, "r")
	str = f.read()
	f.close()
	
	try:
		data = json.loads(str)
	except:
		logging.error("Not JSON (" + str + ")")
		data = {}
	return data

def listDirJSON(dir): # return array of json files in dir
	ret = []

	if not os.path.isdir(dir):
		logging.warning("Dir " + dir + " doesn't exists.")
		return ret

	for filename in os.listdir(dir):
		if filename.endswith(".json"):
			ret.append(filename)

	return ret

def transferFile(filepath, destdir):
	if not os.path.isdir(destdir):
		logging.info("Making directory " + destdir)
		os.makedirs(destdir)

	filepath2 = os.path.join(destdir,os.path.basename(filepath))
	if os.path.isfile(filepath2):
		logging.debug("File " + filepath2 + " exists. Will be replaced.")
		os.remove(filepath2)

	os.rename(filepath,filepath2)
	logging.debug("File " + filepath + " transfered to " + destdir)

def getnum(data,key):
	if key in data and str(data[key]).isdigit():
		return int(data[key])
	else:
		return 0

def getConf():
	return getJSONData("conf.json")

def initLogging():
	# get debug level str from config
	config = getConf()
	levelstr = config['debuglevel'].lower()
	
	# get real debug level
	obj = {
		"debug": logging.DEBUG,
		"info": logging.INFO,
		"warning": logging.WARNING,
		"error": logging.ERROR,
		"critical": logging.CRITICAL
	}

	if not levelstr in obj:
		levelstr = "debug"
		logging.warning("Invalid loginlevel in config.")

	level = obj[levelstr]

	# set it
	logging.basicConfig(level=level,
		format='%(asctime)s %(name)s %(levelname)s %(message)s')