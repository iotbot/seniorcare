#!/usr/bin/env python
#Haotian Wang July 2014
#Read the air quality data from Galileo through serial port
#Usage: ./air.py

import serial
import mosquitto
s = serial.Serial()
s.port = '/dev/ttyS0'
s.open()

mqtt_client=mosquitto.Mosquitto('air')
mqtt_client.connect('127.0.0.1')
air_quality = 0
while 1:
    res = s.readline()
    print 'received: '+res
    print res.find('temp')
    if res.find('temp') != -1:
	temp = res.split()[1]
	print 'temp is '+temp
        temp_data =  float(temp)
        mqtt_client.publish("Test1",'{"name":"temperature","value":"'+str(int(temp_data))+'"}')
    else:
        air_quality = int(float(res.split()[1]))
    mqtt_client.publish("Test1",'{"name":"air_quality","value":"'+str(air_quality)+'"}')
    
