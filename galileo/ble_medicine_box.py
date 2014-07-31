#!/usr/bin/env python

#Haotian Wang.  June 2014 
#Read alarm_time data from mqtt server and control medicine box to raise a alarm
#Usage: ble_medicine_box.py BLUETOOTH_ADR MQTT_SERVER DEVICE_NAME

import pexpect
import sys
import time
#import paho.mqtt.client as paho
import mosquitto
import json
import os

bluetooth_adr = sys.argv[1]
mqtt_server = sys.argv[2]
device_name  = sys.argv[3]
taken_medicine = 0

alarm_time = {} 
alarm_time['0'] = {'0':{'h':8,'m':0,'on':1},'1':{'h':12,'m':0,'on':1},'2':{'h':18,'m':0,'on':1}}
alarm_time['1'] = {'0':{'h':8,'m':0,'on':1},'1':{'h':12,'m':0,'on':1},'2':{'h':18,'m':0,'on':1}}
alarm_time['2'] = {'0':{'h':8,'m':0,'on':1},'1':{'h':12,'m':0,'on':1},'2':{'h':18,'m':0,'on':1}}
alarm_time['3'] = {'0':{'h':8,'m':0,'on':1},'1':{'h':12,'m':0,'on':1},'2':{'h':18,'m':0,'on':1}}
alarm_time['4'] = {'0':{'h':8,'m':0,'on':1},'1':{'h':12,'m':0,'on':1},'2':{'h':18,'m':0,'on':1}}
alarm_time['5'] = {'0':{'h':8,'m':0,'on':1},'1':{'h':12,'m':0,'on':1},'2':{'h':18,'m':0,'on':1}}
alarm_time['6'] = {'0':{'h':8,'m':0,'on':1},'1':{'h':12,'m':0,'on':1},'2':{'h':18,'m':0,'on':1}}
door = []
for i in range(0,21):
    door.append(0)    


def on_message(mosq, userdata, msg):
    global alarm_time
    try:
        json_data = json.loads(str(msg.payload))
        print "json_data: "+str(json_data)
        if json_data['name'] == device_name:
            week = json_data['value']['week'] 
	    meal = json_data['value']['meal']
	    hour = json_data['value']['h']
	    minute = json_data['value']['m']
	    alarm_on = json_data['value']['on']
	    alarm_time[week][meal]['h'] = int(hour)
	    alarm_time[week][meal]['m'] = int(minute)
	    alarm_time[week][meal]['on'] = int(alarm_on)
	    print "alarm time has been changed: week "+week+" meal "+meal+" "+str(alarm_time[week][meal])
    except ValueError:
	print 'parse wrong!'
	return

mqtt_client = mosquitto.Mosquitto(device_name)
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_server)
mqtt_client.subscribe('medicine_box')
tool = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive')
tool.expect('\[LE\]>')
tool.sendline('connect')
if tool.expect('\[CON\].*>') == 0:
    print 'BLE connected!'

while 1:#mqtt_client.loop() == 0: 
    try:
	ret = mqtt_client.loop()
	if ret == 0:
            print 'mqtt listening!'
	else:
	    mqtt_client.unsubscribe('medicine_box')
	    mqtt_client.disconnect()
	    mqtt_client.connect(mqtt_server)
	    mqtt_client.subscribe('medicine_box')
    except Exception,e:
	print 'something wrong!'+str(e)
    try:
	pnum = tool.expect('Notification handle = .*? \r', timeout=50)
    except pexpect.TIMEOUT:
	raise pexpect.TIMEOUT("TIMEOUT")
    if pnum == 0:
	after = tool.after
	data = int(str(after.split()[5]),16)
	hexdata = after.split()[3:]
	print 'data received: '+str(data)
	print 'hex is:'+str(hexdata)
	if data == 50:
	    os.system('echo 1 > /home/root/senior_care/forget_close') #forget to close the door of medicine box
	elif data <= 20 and data >= 0:
	    door[data] = 1 # door is opened!
	    os.system('echo 0  > /home/root/senior_care/alarm_data')
	#elif data <= 41 and data >= 21:
	#    door[data-21] = 0 # door is closed!
		    


    time_now = time.localtime()
    week_now = time.strftime("%w",time_now)
    hour_now = int(time.strftime("%H",time_now))
    min_now = int(time.strftime("%M",time_now))
    sec_now = int(time.strftime("%S",time_now))
    if hour_now == alarm_time[week_now]['0']['h'] and min_now == alarm_time[week_now]['0']['m'] and sec_now == 0 and alarm_time[week_now]['0']['on'] == 1 and door[int(week_now)] == 0:
	print "meal 1!"
	alarm_code = int(week_now)
	print "ALARM: "+str(week_now)
	time.sleep(1)
	if alarm_code > 0:
            tool.sendline('char-write-req 0x0012 0'+hex(int(week_now))[2:])
	else:
            tool.sendline('char-write-req 0x0012 07')
	#os.system('echo 1 > /home/root/senior_care/alarm_data')		
	time.sleep(1)
    elif hour_now == alarm_time[week_now]['1']['h'] and min_now == alarm_time[week_now]['1']['m'] and sec_now == 0 and alarm_time[week_now]['1']['on'] == 1 and door[int(week_now)] == 0:
	alarm_code = int(week_now)
	print "ALARM: "+str(week_now)
	time.sleep(1)
	if alarm_code > 0:
            tool.sendline('char-write-req 0x0012 0'+hex(int(week_now))[2:])
	else:
            tool.sendline('char-write-req 0x0012 07')
#	if alarm_code < 16:
#            tool.sendline('char-write-req 0x0012 0'+hex(alarm_code)[2:])
#	else:
#            tool.sendline('char-write-req 0x0012 '+hex(alarm_code)[2:])
	#os.system('echo 1 > /home/root/maker-contest/test/ready/alarm_data')		
	time.sleep(1)
    elif hour_now == alarm_time[week_now]['2']['h'] and min_now == alarm_time[week_now]['2']['m'] and sec_now == 0 and alarm_time[week_now]['2']['on'] == 1 and door[int(week_now)] == 0:
	alarm_code = int(week_now)
	print "ALARM: "+str(week_now)
	time.sleep(1)
	if alarm_code > 0:
            tool.sendline('char-write-req 0x0012 0'+hex(int(week_now))[2:])
	else:
            tool.sendline('char-write-req 0x0012 07')
#	if alarm_code < 16:
#            tool.sendline('char-write-req 0x0012 0'+hex(alarm_code)[2:])
#	else:
#            tool.sendline('char-write-req 0x0012 '+hex(alarm_code)[2:])
	#os.system('echo 1 > /home/root/maker-contest/test/ready/alarm_data')		
	time.sleep(1)
    if hour_now == alarm_time[week_now]['0']['h'] and min_now == (alarm_time[week_now]['0']['m']+1) and sec_now == 0 and alarm_time[week_now]['0']['on'] == 1 and door[int(week_now)] == 0:
	os.system('echo 1 > /home/root/senior_care/alarm_data')		
	print 'arlarm writen'
    elif hour_now == alarm_time[week_now]['1']['h'] and min_now == (alarm_time[week_now]['1']['m']+1) and sec_now == 0 and alarm_time[week_now]['1']['on'] == 1 and door[int(week_now)] == 0:
	os.system('echo 1 > /home/root/senior_care/alarm_data')		
	print 'arlarm writen'
    elif hour_now == alarm_time[week_now]['2']['h'] and min_now == (alarm_time[week_now]['2']['m']+1) and sec_now == 0 and alarm_time[week_now]['2']['on'] == 1 and door[int(week_now)] == 0:
	os.system('echo 1 > /home/root/senior_care/alarm_data')		
	print 'arlarm writen'
    if hour_now == alarm_time[week_now]['0']['h'] and min_now == (alarm_time[week_now]['0']['m']+5) and sec_now == 0 and alarm_time[week_now]['0']['on'] == 1 and door[int(week_now)] == 0:
	mqtt_client.publish('Test1','{"name":"'+device_name+'","value":"0'+str(week_now)+'0"}')
	mqtt_client.publish('Test1','{"name":"'+device_name+'","value":"0'+str(week_now)+'0"}')
	mqtt_client.publish('Test1','{"name":"'+device_name+'","value":"1'+str(week_now)+'0"}')
	print 'forgot to take medicine//message sent to APP'
    elif hour_now == alarm_time[week_now]['1']['h'] and min_now == (alarm_time[week_now]['1']['m']+5) and sec_now == 0 and alarm_time[week_now]['1']['on'] == 1 and door[int(week_now)] == 0:
	mqtt_client.publish('Test1','{"name":"'+device_name+'","value":"0'+str(week_now)+'1"}')
	mqtt_client.publish('Test1','{"name":"'+device_name+'","value":"0'+str(week_now)+'1"}')
	print 'forgot to take medicine//message sent to APP'
    elif hour_now == alarm_time[week_now]['2']['h'] and min_now == (alarm_time[week_now]['2']['m']+5) and sec_now == 0 and alarm_time[week_now]['2']['on'] == 1 and door[int(week_now)] == 0:
	mqtt_client.publish('Test1','{"name":"'+device_name+'","value":"0'+str(week_now)+'2"}')
	mqtt_client.publish('Test1','{"name":"'+device_name+'","value":"0'+str(week_now)+'2"}')
	print 'forgot to take medicine//message sent to APP'
    if door[int(week_now)-1] == 1 and taken_medicine == 0:
	mqtt_client.publish('Test1','{"name":"'+device_name+'","value":"1'+str(week_now)+'0"}')
	mqtt_client.publish('Test1','{"name":"'+device_name+'","value":"1'+str(week_now)+'0"}')
	print 'have taken medicine//message sent to APP'
	taken_medicine = 1
    if hour_now == 0 and min_now ==0 and sec_now ==0:
	os.system('echo 1 > /home/root/senior_care/day_over')		
	for i in range(0,21):
    	    door[i] = 0   
	taken_medicine = 0 


			
	
