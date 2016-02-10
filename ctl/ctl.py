#!/usr/bin/python

import os
import subprocess
import json
import logging
import utils


def _f(rel):
	cur = os.path.dirname(os.path.realpath(__file__))
	return os.path.join(cur,rel)

def _c(cmd,input=""):
	try:
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
	except BaseException, e:
		logging.error("Ctl: Problem with the command " + str(cmd) + " (" + os.strerror(e.errno) + ")")
		return "",False

	(output,error) = p.communicate(input=input)
	succ = (p.returncode == 0)
	output = output.strip()

	if(error):
		logging.error("Shell: " + error)

	return output,succ

def geturl():
	out, succ = _c([_f("currenturl.sh")])
	return out

def seturl(url):
	out, succ = _c([_f("currenturl.sh"),url])
	return succ

def loadscriptfile(file, include = False):
	a = [_f("loadscript.sh")]
	if(include):
		a += ["-i"]
	a += [file]

	out, succ = _c(a)
	return succ

def loadscriptcode(code, include = False):
	a = [_f("loadscript.sh")]
	if(include):
		a += ["-i"]

	out, succ = _c(a,code)
	return succ

def getdata():
	out, succ = _c([_f("getjson.sh")])
	try:
		data = json.loads(out)
		return data
	except:
		#logging.debug("Ctl: Not JSON. (" + out + ")")
		return {}

def setdata(data):
	code = "var _postappInputData = " + json.dumps(data) + ";"
	return loadscriptcode(code, True)