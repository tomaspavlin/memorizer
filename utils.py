#!/usr/bin/python

import ConfigParser
import logging
import json
import os
import sys

# changes default encoding from ascii. Required for json and files ios
reload(sys)
sys.setdefaultencoding("utf-8")

def stringifyJSON(data):
	ret = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
	#if type(ret) is unicode:
	#	ret = ret.encode("utf8")
	
	return ret


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
	'''
	if key is valid key of int in data, returns it, otherwise returns 0
	'''

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

def getPairsFromFile(file):
    ret = []
    f = open(file,'r')

    for l in list(f):
        l = l.strip()
        arr = l.split("=")
        if(len(arr) == 2):
            ret.append({'first': arr[0].strip(), 'second': arr[1].strip()})
        
    f.close()
    return ret