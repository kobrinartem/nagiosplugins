#!/usr/bin/python2
import os, sys
from optparse import OptionParser
import subprocess

# Exit statuses recognized by Nagios
UNKNOWN = -1
OK = 0
WARNING = 1
CRITICAL = 2

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
status=int(out.split(' ')[3])
if not err:
  if status==1:
    print "OK - UP"
    sys.exit(0);
  elif status==2:
    print "CRITICAL - DOWN"
    raise SystemExit, CRITICAL
  else:
    print "UNKNOWN - UNKNOWN Status"
    raise SystemExit, UNKNOWN
if err:
  print "CRITICAL - %s" % err
  raise SystemExit, CRITICAL
