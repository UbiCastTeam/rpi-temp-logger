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
import requests, json
import os

csv_path = '/var/tmp/temp.csv'
interval_s = 60
NOTEMP = 99999

def gettemp_outside():
    try:
        p = {
            'lat': '48.819598',
            'lon': '2.374334699999963',
            'units': 'metric',
        }
        url = "http://api.openweathermap.org/data/2.5/weather"
        r = requests.get(url, params=p).json()['main']['temp']
        return r
    except Exception as e:
        print('Failed to fetch current outside temperature:\n%s' %e)
        return NOTEMP 

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
      mytemp = NOTEMP 
    f.close()
    return int(mytemp[1])

  except:
    return NOTEMP 

def get_ids():
    p = '/sys/bus/w1/devices/'
    if os.path.isdir(p):
        ids = list()
        d = os.listdir(p)
        for i in d:
            if "_bus_master" not in i:
                ids.append(os.path.basename(i))
        return ids
    return list()

def write_entry(time, temp, temp_yahoo):
    line = "%s,%s,%s\n" %(time, temp, temp_yahoo)
    f = open(csv_path, 'a')
    f.write(line)
    f.close()

if __name__ == '__main__':
  import time
  ids = get_ids()
  sensor_id = ids[0]
  while True:
    now = time.time()
    temp = gettemp(sensor_id)/float(1000)
    temp_outside = gettemp_outside()
    print("Temp of sensor %s : %.2f C, Outside: %s C" %(sensor_id, temp, temp_outside)) 
    write_entry(now, temp, temp_outside)
    time.sleep(interval_s)
