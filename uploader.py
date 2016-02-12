#!/usr/bin/python
# SUMAMRY: Uploads pairs separated with = saved in configured file to Quizlet 
# RETURN CODE: 0 if upload succesful, 1 if nonsuccesful

import utils
import logging
from time import gmtime, strftime
import os
import httplib
import urllib


utils.initLogging()
conf = utils.getConf()

def get_pairs():
    file = conf['uploader']['input']
    return utils.getPairsFromFile(file)

def create_set(name, pairs):
    if(len(pairs) < 2):
        logging.error("Min 2 pairs must be uploaded on quizlet. Number of pairs is %i." % len(pairs))
        return False

    path = "/2.0/sets"
    headers = {
        "Authorization": "Bearer %s" % conf['uploader']['accesstoken'],
        "Content-Type": "application/x-www-form-urlencoded"
    }

    terms = map(lambda p: p['first'], pairs)
    definitions = map(lambda p: p['second'], pairs)

    params = urllib.urlencode({
        "whitespace": "true",
        "title": name,
        "terms[]": terms,
        "definitions[]": definitions,
        "lang_terms": "en",
        "lang_definitions": "cs"
    }, True)

    conn = httplib.HTTPSConnection("api.quizlet.com")
    conn.request("POST", path, params, headers)

    resp = conn.getresponse()
    data = resp.read()

    # if succesful
    if resp.status >= 200 and resp.status < 300:
        return True
    # unsuccesful
    else:
        logging.debug("Quizlet returned: " + data)
        return False

def get_set_name():
    return strftime("Wordlist for %d %b %Y, %a", gmtime())



pairs = get_pairs()
setname = get_set_name()

if create_set(setname, pairs):
    logging.info("{0} pairs uploaded successfully on Quizlet with set name '{1}'".format(len(pairs),setname))
    exit(0)
else:
    logging.error("Uploading on Quizlet unsuccessful")
    exit(1)