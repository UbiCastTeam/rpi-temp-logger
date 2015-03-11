#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Florent Thiery 

from __future__ import print_function

import os
import sys

try:
    fname = sys.argv[1]
except Exception as e:
    print('Please provide csv file argument, exiting')
    sys.exit(1)

if not os.path.isfile(fname):
    print('File not found, exiting')
    sys.exit(1)

import datetime

f = open(fname)
d = f.read()
f.close()

out_file = 'gdoc_%s' %os.path.basename(fname)
f = open(out_file, 'w')
f.write('Date\tTemp\tOutside temp\n')

for line in d.split('\n'):
    fields = line.split(',')
    if len(fields) > 1:
        epoch, temp, outside_temp = float(fields[0]), fields[1], fields[2]
        date = datetime.datetime.fromtimestamp(epoch)
        date_gdoc = date.strftime('%Y/%m/%d %H:%M:%S')
        f.write('%s\t%s\t%s\n' %(date_gdoc, temp.replace('.', ','), outside_temp.replace('.', ',')))
f.close()
print("Wrote %s" %out_file)
