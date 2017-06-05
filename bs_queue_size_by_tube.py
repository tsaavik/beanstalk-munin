#!/usr/bin/env python
"""Reports size of Ready jobs in tubes."""
import os
import sys
import beanstalkc

HOST = os.environ.get('HOST', 'localhost')
PORT = os.environ.get('PORT', 11300)

def clean_tube(tube):
    return tube.replace('.', '_')

def do_data():
    bs = beanstalkc.Connection(HOST, PORT)
    TUBES = bs.tubes()
    for tube in TUBES:
        stats = bs.stats_tube(tube)
        val = stats['current-jobs-ready'] if stats else 0
        print '%s_jobs.value %d' % (clean_tube(tube), val)

def do_config():
    bs = beanstalkc.Connection(HOST, PORT)
    TUBES = bs.tubes()
    print "graph_title Ready Jobs"
    print "graph_vlabel Ready jobs"
    print "graph_category Beanstalk"
    print "graph_args --lower-limit 0"
    print "graph_scale no"
    for tube in TUBES:
        ctube = clean_tube(tube)
        print "%s_jobs.label %s" % (ctube, ctube)
        print "%s_jobs.type GAUGE" % ctube
        print "%s_jobs.min 0" % ctube
        print "%s_jobs.warning 20000 " % ctube
        print "%s_jobs.critical 50000 " % ctube

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'config':
        do_config()
    else:
        do_data()
