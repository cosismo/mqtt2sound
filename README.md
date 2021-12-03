# mqtt2sound

A simple mqtt controlled multitrack 8 tracks player.

It uses pygame and the paho mqtt library.

At launch it start playing the 8 tracks simultaneously in sync, in an infinite loop.
The mqtt messages then control the volume.

The default topic is sound/{channel 0-7} and expects a value between 0 and 1 for the volume.
 
 examples:
 setting volume of cahnnel 3 at 75%
  mosquitto_pub -h 127.0.0.1 -t "sound/3" -m 0.75
  
