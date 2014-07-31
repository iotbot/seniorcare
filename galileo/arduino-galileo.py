#!/usr/bin/env python
#Haotian Wang  June 2014
#Send the 'picture' string to arduino
#Receive the data of PM 2.5 and temperature on arduino
#Usage: arduino-galileo.py MQTT_SERVER

import sys
import time
import mosquitto
import json
import serial
import os

ser = serial.Serial()
ser.port = '/dev/ttyS0'
ser.baudrate = 9600
ser.open()
mqtt_server = sys.argv[1]
old_emergency = '0'

def on_message(mosq, userdata, msg):
    global old_emergency
    json_data = json.loads(str(msg.payload))
    print "json_data: "+str(json_data)
    if json_data['name'] == 'led_array':
        pic = json_data['value']
        print 'pic: '+str(pic)
        #ret = ser.write(str(pic))
        os.system("echo '"+str(pic)+"' > /dev/ttyS0")
        #print str(ret)+' chars have been sent into Serial: '+str(pic)
    elif json_data['name'] == 'light':
	light = json_data['value']
	print 'light: '+str(light)
        os.system("echo 'l"+str(light)+"'$ > /dev/ttyS0")
    elif json_data['name'] == 'steps':
	steps = json_data['value']
	print 'steps: '+str(steps)
        os.system("echo 's"+str(steps)+"'$ > /dev/ttyS0")
    elif json_data['name']== 'emergency':
	print "emergency!!!!  "+json_data['value']
	if json_data['value'] == '1':
	    print "Emergency!"
	    os.system("echo E$ > /dev/ttyS0")
	if json_data['value'] == '0' and old_emergency == '1':
	    os.system("echo e$ > /dev/ttyS0")
	old_emergency = json_data['value']
    elif json_data['name'] == 'falling':
	if json_data['value'] == '1':
	    print 'fall!'
	    os.system("echo F$ > /dev/ttyS0")

	

	


mqtt_client = mosquitto.Mosquitto('arduino-galileo')
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_server)
mqtt_client.subscribe('led_array')

old_alarm = '0'
while 1:
    ret = mqtt_client.loop()
    if ret == 0:
	print 'mqtt listening!'
    else:
	 mqtt_client.unsubscribe('led_array')
         mqtt_client.disconnect()
         mqtt_client.connect(mqtt_server)
         mqtt_client.subscribe('led_array')
    try:
        f_alarm = open('/home/root/senior_care/alarm_data','r+')
    except IOError as err:
        print 'File error '+str(err)
    alarm = f_alarm.read().rstrip()
    f_alarm.close()
    if alarm == '1':
	print 'medicine alarm!'
        os.system("echo 'm' > /dev/ttyS0")
    elif alarm == '0' and alarm != old_alarm:
	print 'medicine alarm cancelled!'
        os.system("echo 'c' > /dev/ttyS0")
    old_alarm = alarm	
    time_now = time.localtime()
    hour_now = int(time.strftime("%H",time_now))
    min_now = int(time.strftime("%M",time_now))
    time_value = hour_now*100+min_now
    os.system("echo 't"+str(time_value)+"'$ > /dev/ttyS0")
	
	


