import socket
import time, sys, os
from pygame import mixer
import ConfigParser

touch = [0,0,0]
sound = [0,0,0]
treshold = [0,0,0]
debounce = [0,0,0]

UDP_IP = "7.7.7.1"
UDP_PORT = 3333

config = ConfigParser.ConfigParser()
config.read("/home/pi/RemoteTouch/sounds/config.txt")
treshold[0] = int(config.get("tresholds", "treshold_0"))
treshold[1] = int(config.get("tresholds", "treshold_1"))
treshold[2] = int(config.get("tresholds", "treshold_2"))

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

mixer.init()
mixer.set_num_channels(6)
sound0 = mixer.Sound("/home/pi/RemoteTouch/sounds/zone0.wav")
sound1 = mixer.Sound("/home/pi/RemoteTouch/sounds/zone1.wav")
sound2 = mixer.Sound("/home/pi/RemoteTouch/sounds/zone2.wav")
sound3 = mixer.Sound("/home/pi/RemoteTouch/sounds/zone3.wav")

chan0=mixer.Channel(0)
chan1=mixer.Channel(1)
chan2=mixer.Channel(2)
chan3=mixer.Channel(3)

while True:
   sound0.set_volume(0)
   sound1.set_volume(0)
   sound2.set_volume(0)
   sound3.set_volume(1)
   chan0.play(sound0)
   chan1.play(sound1)
   chan2.play(sound2)
   chan3.play(sound3)

   while mixer.get_busy():
      data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

      touch[ord(data[0])] = ord(data[1])
      if touch[ord(data[0])] < treshold[0]:
         debounce[ord(data[0])]=debounce[ord(data[0])]+1
         if debounce[ord(data[0])] > 2:
            sound[ord(data[0])] = 1
            print "touch"
      else:
         sound[ord(data[0])] = 0
         debounce[ord(data[0])]=0

      sound0.set_volume(sound[0])
      sound1.set_volume(sound[1])
      sound2.set_volume(sound[2])

      print ("Sensor 0:", touch[0], "  Sensor 1: ", touch[1] , "  Sensor 2: ", touch[2])

   print "EOF, loop"
