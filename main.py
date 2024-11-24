try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network
import start_state
import os
import time

START_STATE = 1
MONITOR_STATE = 2

state = START_STATE # DEBUG
SSID = 'NONE'
PASSWORD = 'NONE'


# --- Get connection data---
if 'ssid.txt' in os.listdir():
  f = open('ssid.txt', 'r')
  SSID = f.read()
  f.close()

if 'pwd.txt' in os.listdir():
  f = open('pwd.txt', 'r')
  PASSWORD = f.read()
  f.close()

# --- Try to connect ---
#wlan = network.WLAN(network.STA_IF)

#wlan.active(True)
#wlan.connect(SSID, PASSWORD)

#wait_time = time.ticks_ms() + 5000
 
#while wlan.isconnected() == False:
#  if wait_time < time.ticks_ms():
#    state = START_STATE
#    break

if state == START_STATE:
  print('Not connected - Start procedure')
  # Must have: Temperature, ON/OFF button, ssid/pwd
  wlan = network.WLAN(network.AP_IF)
  wlan.active(0)
  wlan.config(ssid='aqua_mon')
  wlan.active(1)
  print(wlan.ifconfig())
  

  start_state.start_state()
else:
  print('Connection successful')
  print(wlan.ifconfig())
