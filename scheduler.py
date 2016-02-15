#!/usr/bin/python
"""
This program is http server that can be used for saving text into text file 
"""

import utils
import logging
import time
import datetime
import sys
import random
import codecs


utils.initLogging()

conf = utils.getConf()

file_data = conf["scheduler"]['files']['data']
file_new = conf["scheduler"]['files']['new']
file_upload = conf["scheduler"]['files']['upload']
min_count = int(conf["scheduler"]['min_count'])
max_count = int(conf["scheduler"]['max_count'])
max_delay = int(conf["scheduler"]['max_delay'])
file_time = conf["scheduler"]['files']['time']


def is_sooner_than(t1,t2):
    return t1 <= t2 + 3600

def increase_time_file():
    return
    #f = open(file_time,"r")
    #time = int(f.readline())
    #f.close()

    #time += 1

    #f = open(file_time,"w")
    #f.write(str(time))
    #f.close()

def get_time_from_delay(delay):
    # delay is in days

    #f = open(file_time,"r")
    #time = int(f.readline())
    #f.close()

    #ret = time
    #ret += delay

    ret = time.time()
    ret += delay*3600*24

    return ret

def get_new_data():
    pairs = utils.getPairsFromFile(file_new)
    ret = []
    for p in pairs:
        obj = {
            "first": p['first'],
            "second": p['second'],
            "state": "planned",
            "delay": 0,
            "time_plan": get_time_from_delay(0),
            "time_added": get_time_from_delay(0)
        }

        ret.append(obj)

    return ret

def split_data_for_upload(data):
    upload = []
    noupload = []

    for d in data:
        if d['state'] == 'planned' and is_sooner_than(d['time_plan'],get_time_from_delay(0)):
            upload.append(d)
        else:
            noupload.append(d)
    if len(upload) < min_count:
        logging.warning("Only %i items planned for today, minimum is %i" % (len(upload), min_count))
        return ([],data)

    if len(upload) > max_count:
        logging.info("%i items planned for today but choosing only %i of them" % (len(upload), max_count))

        random.shuffle(upload)
        noupload += upload[max_count:]
        upload = upload[:max_count]

    return (upload, noupload)

def save_data_for_upload(data):
    f = open(file_upload,"w")

    for d in data:
        #d['first'] = d['first'].encode("utf-8")
        #d['second'] = d['second'].encode("utf-8")
        #print d['first']
        #print d['second']
        #print type(d['first'])
        #print type(d['second'])
        str = "{0:s} = {1:s}\n".format(
            d['first'],
            d['second']
        )
        
        #str_u = str.decode("utf8")

        f.write(str)

    f.close()

def postpone_data(data):
    ret = []
    done_count = 0
    for a in data:
        if a['delay'] >= max_delay:
            a['state'] = 'done'
            done_count += 1
        else:
            if a['delay'] == 0:
                a['delay'] = 1
            else:
                a['delay'] *= 2

            a['time_plan'] = get_time_from_delay(a['delay'])

        ret.append(a)

    if done_count > 0:
        logging.info("%i items marked as done" % done_count)

    return ret

def save_data(data):
    str = utils.stringifyJSON(data)
    
    #print str
    #print type(str)

    #str_u = str.decode("utf8")

    f = open(file_data,"w")
    f.write(str)
    f.close()

# status
if len(sys.argv) == 2 and sys.argv[1] == "status":
    print "TODO"

    exit(0)

stats = {}

# default
# get data for processing
data = utils.getJSONData(file_data)
data_new = get_new_data()
data += data_new


logging.debug("Found %i new items" % len(data_new))
conf['all'] = len(data)
conf['new'] = len(data_new)

# split data by upload
upload, noupload = split_data_for_upload(data)

# process data for upload
save_data_for_upload(upload)
upload = postpone_data(upload)

logging.debug("%i items saved for upload" % len(upload))
conf['upload'] = len(upload)

# save data file
data = noupload + upload
save_data(data)

# empty file_new
open(file_new,"w").close()

# increase time file
increase_time_file()

logging.info("Found {0} new items. There are {1} items overall, {2} scheduled for today."
    .format(conf['new'],conf['all'],conf['upload']))


