#!/usr/bin/python
import pygame
import os

import paho.mqtt.client as mqtt


# set up the mixer at 44100 frequency, with 16 signed bits per sample, 1 channel, with a 2048 sample buffer
pygame.mixer.init(44100, -16, 1, 2048)

currently_playing_file = ""


def on_message(mqttc, obj, msg):
    print ("Received %s on topic %s" % (msg.payload, msg.topic))
    alarm = int(msg.payload)
    print(alarm)
    if alarm == 1:
        play("goatBaa.wav")
    elif alarm == 2:
        play("cockCalling.wav")
    elif alarm == 3:
        play("horseNeighing.wav")
    elif alarm == 4:
        play("lionRoar.wav")
    elif alarm == 5:
        play("ravenCalling.wav")

def play(filename,level = 1.0):
    global currently_playing_file
    if os.path.isfile(filename):
        if (not pygame.mixer.music.get_busy()) or (currently_playing_file is not filename):
            print ("Playing %s" % filename)
            currently_playing_file = filename
            pygame.mixer.music.load(filename)
            pygame.mixer.music.set_volume(level)
            pygame.mixer.music.play()


mqttc = mqtt.Client()
mqttc.connect("127.0.0.1", 1883, 60)

mqttc.subscribe("/alarm")

mqttc.on_message = on_message

mqttc.loop_forever()

#while mqttc.loop(timeout=100) == 0:
 
#   pass

