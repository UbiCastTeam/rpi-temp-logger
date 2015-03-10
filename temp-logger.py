#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------
#
#              ds18b20.py
#  Read DS18B20 1-wire temperature sensor
#
# in /boot/config.txt:
#dtoverlay=w1-gpio,gpiopin=4
#
# Author : Matt Hawkins
# Date   : 10/02/2015
#
# http://www.raspberrypi-spy.co.uk/
# http://www.raspberrypi-spy.co.uk/2013/03/raspberry-pi-1-wire-digital-thermometer-sensor/
#
#--------------------------------------

from __future__ import print_function
import os

def gettemp(id):
  try:
    mytemp = ''
    filename = 'w1_slave'
    f = open('/sys/bus/w1/devices/' + id + '/' + filename, 'r')
    line = f.readline() # read 1st line
    crc = line.rsplit(' ',1)
    crc = crc[1].replace('\n', '')
    if crc=='YES':
      line = f.readline() # read 2nd line
      mytemp = line.rsplit('t=',1)
    else:
      mytemp = 99999
    f.close()
    return int(mytemp[1])

  except:
    return 99999

def get_ids():
    p = '/sys/bus/w1/devices/'
    ids = list()
    d = os.listdir(p)
    for i in d:
        if "_bus_master" not in i:
            ids.append(os.path.basename(i))
    return ids

def write_entry(time, temp):
    line = "%s,%s\n" %(time, temp)
    f = open('/var/tmp/temp', 'a')
    f.write(line)
    f.close()

if __name__ == '__main__':
  import time
  # Script has been called directly
  ids = get_ids()
  while True:
      for i in ids:
        temp = gettemp(i)/float(1000)
        now = time.time()
        print("Temp of sensor %s : %.2f C" %(i, temp)) 
        write_entry(now, temp)
        time.sleep(30)
