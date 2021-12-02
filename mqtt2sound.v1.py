#!/usr/bin/python
import time
from pygame import mixer
import os
import paho.mqtt.client as mqtt


#sound = [ 0, 0, 0, 0 ]
soundVol = [ 1, 1, 1, 1, 1, 1, 1, 1 ]

# set up the mixer at 44100 frequency, with 16 signed bits per sample, 1 channel, with a 2048 sample buffer
mixer.init(44100, -16, 1, 2048)

currently_playing_file = ""


def on_message(mqtcc, obj, msg):
    print ("Received %s on topic %s" % (msg.payload, msg.topic))
    for i in range (4):
        if msg.topic == 'sound/' + str(i):
            soundVol[i] = int(msg.payload)


mqttc = mqtt.Client()
mqttc.connect("127.0.0.1",1883,60)

mqttc.subscribe("sound/#")

mqttc.on_message = on_message
mqttc.loop_start()

mixer.init()
mixer.set_num_channels(8)
sound0 = mixer.Sound("/home/pi/mqtt2sound/sounds/zone0.wav")
sound1 = mixer.Sound("/home/pi/mqtt2sound/sounds/zone1.wav")
sound2 = mixer.Sound("/home/pi/mqtt2sound/sounds/zone2.wav")
sound3 = mixer.Sound("/home/pi/mqtt2sound/sounds/zone3.wav")

chan0=mixer.Channel(0)
chan1=mixer.Channel(1)
chan2=mixer.Channel(2)
chan3=mixer.Channel(3)

while True:
   sound0.set_volume(0)
   sound1.set_volume(0)
   sound2.set_volume(0)
   sound3.set_volume(0)
   chan0.play(sound0)
   chan1.play(sound1)
   chan2.play(sound2)
   chan3.play(sound3)

   while mixer.get_busy():
      sound0.set_volume(soundVol[0])
      sound1.set_volume(soundVol[1])
      sound2.set_volume(soundVol[2])
      sound3.set_volume(soundVol[3])

      print ("sound 0:", soundVol[0], "  sound 1: ", soundVol[1] , "  sound 2: ", soundVol[2], "  sound 3: ", soundVol[3] )
      time.sleep(1)
   print ("EOF, loop")
