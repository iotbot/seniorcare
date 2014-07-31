#!/usr/bin/env python

#Haotian Wang.  May 2014
#Read data from BLE on Arduino
#Usage: ble_test.py BLUETOOTH_ADR MQTT_SERVER

import pexpect
import sys
import time
import mosquitto
import os

alarm_cnt = 0
day_over_cnt = 0

mqtt_client = mosquitto.Mosquitto("pulse_sensor") 

def mosquitto_on_publish(mosq, userdata, mid):
    pass#mosq.disconnect()

mqtt_client.on_publish = mosquitto_on_publish


def floatfromhex(h):
    t = float.fromhex(h)
    if t > float.fromhex('7FFF'):
        t = -(float.fromhex('FFFF') - t)
        pass
    return t

bluetooth_adr = sys.argv[1]
mqtt_server = sys.argv[2]

#try:
#    f_alarm = open('/home/root/senior_care/alarm_data','r+')
#    f_day_over = open('/home/root/senior_care/day_over','r+')
#except IOError as err:
#    print 'File Error:'+str(err)

tool = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive')
tool.expect('\[LE\]>')
tool.sendline('connect')
# test for success of connect
if tool.expect('\[CON\].*>') == 0:
	print "BLE connected!"

mqtt_client.connect('localhost')
while True:
	try:
		pnum = tool.expect('Notification handle = .*? \r', timeout=50)
	except pexpect.TIMEOUT:
		raise pexpect.TIMEOUT("TIMEOUT")
	if pnum == 0:
		after = tool.after
		hexstr = after.split()[3:]
		print 'hexdata: '+str(hexstr)
		fall = int(str(after.split()[5]),16)
		steps = int(str(after.split()[6]),16)
		pulse = int(str(after.split()[7]),16)
		photo_time = int(str(after.split()[8]),16)
		emergency = int(str(after.split()[9]),16)
		print 'fall steps hr pt em: '+str(fall)+' '+str(steps)+' '+str(pulse)+' '+str(photo_time)+' '+str(emergency)
		#the data of pulse
		mqtt_client.connect(mqtt_server)
		mqtt_client.publish('Test1','{"name":"pulse", "value":'+str(pulse)+'}')
		mqtt_client.publish('Test1','{"name":"falling", "value":"'+str(fall)+'"}')
		mqtt_client.publish('Test1','{"name":"steps", "value":"'+str(steps)+'"}')
		mqtt_client.publish('Test1','{"name":"phototime", "value":"'+str(photo_time)+'"}')
		mqtt_client.publish('Test1','{"name":"emergency", "value":"'+str(emergency)+'"}')
		mqtt_client.publish('led_array','{"name":"steps", "value":'+str(steps)+'}')
		mqtt_client.publish('led_array','{"name":"light", "value":'+str(photo_time)+'}')
		mqtt_client.publish('led_array','{"name":"emergency", "value":"'+str(emergency)+'"}')
		mqtt_client.publish('led_array','{"name":"falling", "value":"'+str(fall)+'"}')
		
	else:
		print "TIMEOUT!!"

	try:
    	    f_alarm = open('/home/root/senior_care/alarm_data','r+')
    	    f_day_over = open('/home/root/senior_care/day_over','r+')
	except IOError as err:
    		print 'File Error:'+str(err)
	alarm = f_alarm.read().rstrip()
	day_over = f_day_over.read().rstrip()
	f_alarm.close()
	f_day_over.close()
	
	#tool.sendline('char-write-req 0x0012 0'+alarm+' 0'+day_over)
	if alarm == '0' and day_over == '0':
	    tool.sendline('char-write-req 0x0012 41')
	    print 'sending signal A'
	if alarm == '1' and day_over == '0':
	    tool.sendline('char-write-req 0x0012 42')
	    print 'sending signal B'
	if alarm == '0' and day_over == '1':
	    tool.sendline('char-write-req 0x0012 43')
	    print 'sending signal C'
	if alarm == '1' and day_over == '1':
	    tool.sendline('char-write-req 0x0012 44')
	    print 'sending signal D'

	print 'alarm & day over data: 0'+str(alarm)+' 0'+str(day_over)
	if alarm == '1' and alarm_cnt == 90:
	    os.system('echo 0 > /home/root/senior_care/alarm_data')
	    alarm_cnt = 0
	if day_over == '1' and day_over_cnt == 90:
	    os.system('echo 0 > /home/root/senior_care/day_over')
	    day_over = 0
	if alarm == '1' and alarm_cnt < 90:
	    alarm_cnt += 1
	if day_over == '1' and day_over_cnt < 90:
	    day_over_cnt += 1



