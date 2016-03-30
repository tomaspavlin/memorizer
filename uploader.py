#!/usr/bin/python
"""
Program for manipulating between local wordlists in files and Quizlet sets

Reads tasks in config file and processes them. There are these types of tasks:
- remove
- create
- remove_create

For more usage info read either config file or this file.
"""

import utils
import logging
from time import gmtime, strftime
import quizlet

utils.initLogging()
conf = utils.getConf()

def transoform_setname(setname):
    return strftime(setname, gmtime())

def do_task_remove_create(setname, pairfile):
    do_task_remove(setname)
    return do_task_create(setname, pairfile)

def do_task_remove(setname):
    c = quizlet.remove_sets_by_title(setname)
    logging.debug("Removed {0} sets with name '{1}'".format(c, setname))

def do_task_create(setname, pairfile):
    pairs = utils.getPairsFromFile(pairfile)
    
    suc = quizlet.create_set(setname,pairs)

    if suc:
        logging.debug("Set '{0}'' created on Quizlet with pairfile '{1}'' with {2} pairs".format(setname, pairfile, len(pairs)))
    else:
        logging.error("Unsuccessful creating of Quizlet set '{0}' with pairfile '{1}'".format(setname, pairfile))

    return suc

tasks = conf['uploader']['tasks']

errc = 0
succ = 0

# process all tasks
for task in tasks:
    # get task params
    type = task['type']
    setname = task['setname'] if 'setname' in task else ""
    pairfile = task['pairfile'] if 'pairfile' in task else ""
    setname = transoform_setname(setname)

    logging.debug("Processing task '{0}' with args '{1}', '{2}'".format(type, setname, pairfile))
    # process task
    if type == "remove":
        do_task_remove(setname)
        succ += 1
    elif type == "create":
        if do_task_create(setname, pairfile):
            succ += 1
        else: errc += 1
    elif type == "remove_create":
        if do_task_remove_create(setname, pairfile):
            succ += 1
        else: errc += 1
    elif type == "none":
        succ += 1
    else:
        logging.error("Invalid taks type '{0}'".format(type))
        errc += 1

logging.info("{0} uploader tasks succesful, {1} unsuccesful".format(succ, errc))