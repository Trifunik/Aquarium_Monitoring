try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import wifi_login

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = wifi_login.SSID
password = wifi_login.PASSWORD

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin(2, Pin.OUT)
