#!/usr/bin/python

import utils
import logging
import time
import os
from ctl import ctl
import BaseHTTPServer
from urlparse import urlparse, parse_qs



utils.initLogging()

conf = utils.getConf()

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/plain")
        s.end_headers()
    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "text/plain")
        s.end_headers()

        params = parse_qs(urlparse(s.path).query)

        if('text' in params and
        	len(params['text']) == 1 and
        	write_line(params['text'][0]) and
        	'pass' in params and
        	len(params['pass']) == 1 and
        	params['pass'][0] == conf['server']['pass']
        	):
        	
    		s.wfile.write("succ")
    	else:
    		s.wfile.write("err")

def start_server(host_name, port_number):
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((host_name, port_number), MyHandler)
    logging.info("Server %s:%s started." % (host_name, port_number))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info("Server %s:%s stopped." % (host_name, port_number))

def write_line(line):
	logging.debug("Writing line %s..." % line)

	try:
		f = open(conf['server']['output'],'a')
		f.write(line)
		f.write("\n")
		f.close()

		logging.debug("Written.")
		return True

	except:
		logging.error("Error occured while writing to file.")
		return False


host = conf['server']['host']
port = int(conf['server']['port'])

start_server(host, port)
