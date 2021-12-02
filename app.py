#!/usr/bin/python
import time
from pygame import mixer
import os
import paho.mqtt.client as mqtt


#soundsFolder = "/home/pi/media/sounds/";
soundsFolder = "/media/usb1/";
sound = [ ]
chan = [ ]
soundVol = [ 0, 0, 0, 0, 0, 0, 0, 0 ]

# set up the mixer at 44100 frequency, with 16 signed bits per sample, 1 channel, with a 2048 sample buffer
mixer.init(44100, -16, 1, 2048)

currently_playing_file = ""


def on_message(mqtcc, obj, msg):
    #print ("Received %s on topic %s" % (msg.payload, msg.topic))
    for i in range (8):
        if msg.topic == 'sound/' + str(i):
            soundVol[i] = int(msg.payload)

mqttc = mqtt.Client()
mqttc.connect("127.0.0.1",1883,60)

mqttc.subscribe("sound/#")

mqttc.on_message = on_message
mqttc.loop_start()

mixer.init()
mixer.set_num_channels(8)
for i in range (8):
   try:
     sound.append(mixer.Sound(soundsFolder + "zone" + str(i) + ".wav"))
     chan.append(mixer.Channel(i))
   except:
      print("oops")


while True:
   for i in range (8):
      try:
        sound[i].set_volume(0)
        chan[i] = mixer.Channel(i)
        chan[i].play(sound[i])
      except:
         print("oops")

   while mixer.get_busy():
     for i in range (8):
       try:
         sound[i].set_volume(soundVol[i])
       except:
         print("oops")

#     print ("soundVol :", str(soundVol))

     #for i in range (8):
     #  print ("sound " + str(i) + ":", str(soundVol[i]) + ",  " )

#     print("\n")
     time.sleep(0.1)
#   print ("EOF, loop")
