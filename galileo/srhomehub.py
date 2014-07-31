# coding: UTF-8
from ctypes import *
import os
import sys
import time
import mosquitto
import json
from subprocess import *

class sphinx():
    def __init__(self):
        self.sphinx = cdll.LoadLibrary("/usr/lib/libpocketsphinx.so.1")

    def prepare(self, configfile):
        return self.sphinx.soundrecognize_from_mic_init(configfile)

    def start_recognize(self, result):
        return self.sphinx.soundrecognize_from_mic_onetime(result)

    def close(self):
        return self.sphinx.soundrecognize_from_mic_close()

def mqttsr_publish(mosq, obj, mid):
    print("Message" + str(mid)+ " published")

def main():
    language = "chinese"
    configfile = "/usr/share/pocketsphinx/homehub_chn.conf"
    mqtt_server = "127.0.0.1"
    result = create_string_buffer(64)

    running = True
    list_command = True

    if len(sys.argv) > 1:
        if sys.argv[1] == "chinese" or sys.argv[1] == "chn":
            language = "chinese"
        elif sys.argv[1] == "eng" or sys.argv[1] == "english":
            language = "english"

    if len(sys.argv) > 2:
        mqtt_server = sys.argv[2]

    if language == "chinese":
        configfile = "/usr/share/pocketsphinx/homehub_chn.conf"
    else:
        configfile = "/usr/share/pocketsphinx/senior_care_eng.conf"

    mqtt_sr = mosquitto.Mosquitto("sr")
    mqtt_sr.connect(mqtt_server)
    mqtt_sr.on_publish = mqttsr_publish

    print "Voice recognition initializing..."
    sr = sphinx()
    ret = sr.prepare(configfile)
    if ret < 0:
        print "Voice recognition prepare failed"
        sr.close()

    if list_command:
        if language == "chinese":
            print "支持语言: 中文"
            print "支持命令: 我要出门 开灯 红色灯 绿色灯 拍照"
            print "          我出门了 关灯 蓝色灯 紫色灯"
        else:
            print "Language:english"
            print "Supported command list: I'm going out"
            print "                        I'm back"

    while running:
        ret = sr.start_recognize(result)
        if ret < 0:
            running = False
        # get the recognized text
        else:
            print "Recognized text:", result.value
            if language == "chinese":
                if result.value == "我要出门" or result.value == "我出门了":
                    mqtt_sr.connect(mqtt_server)
                    mqtt_sr.publish('homehub/human', '{"name":"human","property":"status","action":"report","value":"leave","type":"string"}')
                elif result.value == "开灯":
                    mqtt_sr.connect(mqtt_server)
                    mqtt_sr.publish('homehub/human', '{"name":"human","property":"control","action":"report","value":"light on","type":"string"}')
                elif result.value == "关灯":
                    mqtt_sr.connect(mqtt_server)
                    mqtt_sr.publish('homehub/human', '{"name":"human","property":"control","action":"report","value":"light off","type":"string"}')
                elif result.value == "红色灯":
                    mqtt_sr.connect(mqtt_server)
                    mqtt_sr.publish('homehub/human', '{"name":"human","property":"control","action":"report","value":"light red","type":"string"}')
                elif result.value == "蓝色灯":
                    mqtt_sr.connect(mqtt_server)
                    mqtt_sr.publish('homehub/human', '{"name":"human","property":"control","action":"report","value":"light blue","type":"string"}')
                elif result.value == "绿色灯":
                    mqtt_sr.connect(mqtt_server)
                    mqtt_sr.publish('homehub/human', '{"name":"human","property":"control","action":"report","value":"light green","type":"string"}')
                elif result.value == "黄色灯":
                    mqtt_sr.connect(mqtt_server)
                    mqtt_sr.publish('homehub/human', '{"name":"human","property":"control","action":"report","value":"light yellow","type":"string"}')
                elif result.value == "拍照":
                    mqtt_sr.connect(mqtt_server)
                    mqtt_sr.publish('homehub/human', '{"name":"human","property":"control","action":"report","value":"take picture","type":"string"}')

            else:
                if result.value == "I AM GOING OUT" or result.value == "I'M GOING OUT":
                    mqtt_sr.connect(mqtt_server)
	            mqtt_sr.publish('homehub/human', '{"name":"human","property":"status","action":"report","value":"leave","type":"string"}')	
		if result.value == "LIGHT":
		    print 'light...'
		    os.system("echo L$ > /dev/ttyS0")
		if result.value == "STEPS":
		    print 'step...'
		    os.system("echo S$ > /dev/ttyS0")
		if result.value == "PICTURE":
		    print 'picture...'
		    os.system("echo P$ > /dev/ttyS0")
		if result.value == "TIME":
		    print 'time...'
		    os.system("echo T$ > /dev/ttyS0")
		

    sr.close()
    mqtt_sr.disconnect()

if __name__=='__main__':
    main()

