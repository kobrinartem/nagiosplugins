#!/usr/bin/python2
import os, sys
from optparse import OptionParser
import subprocess

# I'm going to be using optparse.OptionParser from now on.  It makes
# command-line args a breeze.
parser = OptionParser()
parser.add_option('-H', '--hostname', dest='hostname')
parser.add_option('-o', '--oid', dest='oid')

options, args = parser.parse_args()

# Check for required options
for option in ('hostname', 'oid'):
    if not getattr(options, option):
        print 'CRITICAL - %s not specified' % option.capitalize()
        raise SystemExit, CRITICAL

st=subprocess.Popen(["snmpget", "-v", "1", "-c", "public", options.hostname, options.oid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = st.communicate()
#print "out:", out
#print "err:", err

if not err:
  net_rate=int(out.split(' ')[3])/60
  print "OK - %i kByte/s " % net_rate
if err:
  print "CRITICAL - %s" % err
