# rpi-temp-logger
DS18B20 based simple temperature logger for the Raspberry Pi

Based off Matt Hawkins's code 
http://www.raspberrypi-spy.co.uk/2013/03/raspberry-pi-1-wire-digital-thermometer-sensor/

Tested on Arch Linux

## Install

Add the following to /boot/config.txt
```dtoverlay=w1-gpio,gpiopin=4```

Put temp-logger.py into /usr/bin, and temp-logger.service into /etc/systemd/system/multi-user.target.wants
