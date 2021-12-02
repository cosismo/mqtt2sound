#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2010-2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# Copyright (c) 2010,2011 Roger Light <roger@atchoo.org>
# All rights reserved.

# This shows a simple example of an MQTT subscriber.

#import context  # Ensures paho is in PYTHONPATH
import pygame
import os
import paho.mqtt.client as mqtt


# set up the mixer at 44100 frequency, with 16 signed bits per sample, 1 channel, with a 2048 sample buffer
pygame.mixer.init(44100, -16, 1, 2048)

currently_playing_file = ""



def play(filename,level = 1.0):
    global currently_playing_file
    if os.path.isfile(filename):
        if (not pygame.mixer.music.get_busy()) or (currently_playing_file is not filename):
            print ("Playing %s" % filename)
            currently_playing_file = filename
            pygame.mixer.music.load(filename)
            pygame.mixer.music.set_volume(level)
            pygame.mixer.music.play()

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


#def on_message(mqttc, obj, msg):
#    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
def on_message(mqtcc, obj, msg):
    print ("Received %s on topic %s" % (msg.payload, msg.topic))
    cmd = msg.payload.decode("utf-8") 
    if cmd == "1":
        print("goatBaa.wav")
        play("goatBaa.wav")
    elif cmd == '2':
        play("cockCalling.wav")
    elif cmd == '3':
        play("horseNeighing.wav")
    elif cmd == '4':
        play("lionRoar.wav")
    elif cmd == '5':
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


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect("127.0.0.1", 1883, 60)
mqttc.subscribe("sound", 0)

mqttc.loop_forever()
