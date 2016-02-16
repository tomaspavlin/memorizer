#!/usr/bin/python
"""
This program is http server that can be used for saving text into text file

(...)
"""

import utils
import logging
import time
import os
import BaseHTTPServer
from urlparse import urlparse, parse_qs
import quizlet


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
        	'pass' in params and
        	len(params['pass']) == 1 and
        	params['pass'][0] == conf['server']['pass'] and
            write_line(params['text'][0])
        	):
        	   s._on_succ_write()
    		
    	else:
    		s.wfile.write("err")
            logging.error("Error occured in http request.")

    def _on_succ_write(s):
        s.wfile.write("succ")

        fname = conf['server']['output']
        setname = conf['server']['setname']

        pairs = utils.getPairsFromFile(fname)

        quizlet.remove_sets_by_title(setname)
        if quizlet.create_set(setname, pairs):
            logging.info("Quizlet set '{0}' updated. There are {1} items in that set now.".format(setname,len(pairs)))
        else:
            logging.error("Updating {1} items in Quizlet set '{0}' unsuccesful.".format(setname,len(pairs)))


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
