#!/usr/bin/python
"""
This library implements some api functions for quizlet
"""

import utils
import logging
import os
import httplib
import urllib
import json

utils.initLogging()
conf = utils.getConf()


def _get_quizlet_response(method, path, params):
    accesstoken = conf['quizlet']['accesstoken']

    headers = {
        "Authorization": "Bearer %s" % accesstoken,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    conn = httplib.HTTPSConnection("api.quizlet.com")

    conn.request(method, path, params, headers)
    resp = conn.getresponse()
    return resp

def create_set(title, pairs):
    """
    Create new set with title and imports pairs in it.

    Pairs are in form [{'first':'??', 'second':'??'}, ..]
    Returns True if succesful.
    """

    if(len(pairs) < 2):
        logging.error("Min 2 pairs must be uploaded on quizlet. Number of pairs is %i." % len(pairs))
        return False


    # set arguments
    path = "/2.0/sets"
    method = "POST"
    
    terms = map(lambda p: p['first'], pairs)
    definitions = map(lambda p: p['second'], pairs)
    params = urllib.urlencode({
        "whitespace": "true",
        "title": title,
        "terms[]": terms,
        "definitions[]": definitions,
        "lang_terms": "en",
        "lang_definitions": "cs"
    }, True)

    # get data
    try:
        resp = _get_quizlet_response(method, path, params)
    except:
        logging.debug("Error occured while requesting Quizlet server.")
        return False

    data = resp.read()

    # if succesful
    if resp.status >= 200 and resp.status < 300:
        return True
    # unsuccesful
    else:
        logging.debug("Quizlet returned: " + data)
        return False

def get_sets_by_title(title):
    uid = conf['quizlet']['uid']
    """
    Gets all data of sets which title contains title
    """

    # set arguments
    path = "/2.0/users/"+uid+"/sets"
    method = "GET"
    params = ""

    # get data
    try:
        resp = _get_quizlet_response(method, path, params)
    except:
        logging.debug("Error occured while requesting Quizlet server.")
        return []

    data = json.loads(resp.read())


    # if succesful
    if resp.status >= 200 and resp.status < 300:
        ret = [s for s in data if (title in s['title'])]
        return ret
    # unsuccesful
    else:
        logging.debug("Quizlet returned: " + data)
        return []

def add_terms_into_set_by_id(sid, pair):
    """
    Add pair into set found by id.

    Pair is in form {'first':'??', 'second':'??'}
    Returns True if succesful.
    """


    # set arguments
    path = "/2.0/sets/"+str(sid)+"/terms"
    method = "POST"

    params = urllib.urlencode({
        "whitespace": "true",
        "term": pair['first'],
        "definition": pair['second']
    }, True)

    # get data
    try:
        resp = _get_quizlet_response(method, path, params)
    except:
        logging.debug("Error occured while requesting Quizlet server.")
        return False

    data = resp.read()

    # if succesful
    if resp.status >= 200 and resp.status < 300:
        return True
    # unsuccesful
    else:
        logging.debug("Quizlet returned: " + data)
        return False

def remove_sets_by_title(title):
    """
    Remove all sets which title equals to title and returns number of them
    """

    ids = [s['id'] for s in get_sets_by_title(title)]

    errc = 0
    succ = 0

    for id in ids:
        # set arguments
        path = "/2.0/sets/"+str(id)
        method = "DELETE"
        params = ""

        # get data
        try:
            resp = _get_quizlet_response(method, path, params)
            data = resp.read()

            if resp.status >= 200 and resp.status < 300:
                succ += 1
            else:
                logging.debug("Quizlet returned: " + data)
                errc += 1
        except:
            logging.debug("Error occured while requesting Quizlet server.")
            errc += 1        

    return succ

#if __name__ == "__main__":
    #create_set("Just added wordlist",[{'first':'a','second':'b'},{'first':'a','second':'b'}])
    #get_sets_by_title("Just added wordlist")
    #add_terms_into_set_by_id(121688120, {"first": "ahoj", "second": "cau"})
    #print remove_sets_by_title("abc")