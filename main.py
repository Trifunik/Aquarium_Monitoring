try:
  import usocket as socket
except:
  import socket

import machine
import network
import start_state
import monitoring_state
import os
import time

state = 'MONITOR_STATE'
ssid = 'NONE'
password = 'NONE'

# --- Check State ---
if 'state.txt' in os.listdir():
  f = open('state.txt', 'r')
  state = f.read()
  print(state)
  f.close()

if state == 'START_STATE':
  print('Not connected - Start procedure')
  # Must have: Temperature, ON/OFF button, ssid/pwd
  wlan = network.WLAN(network.AP_IF) # create access-point interface
  wlan.config(ssid='AQUA') # set the SSID of the access point
  wlan.config(max_clients=10) # set how many clients can connect to the network
  wlan.active(True)         # activate the interface

  print(wlan.ifconfig())

  start_state.start_state()

else:
  # --- Get connection data---
  if 'ssid.txt' in os.listdir():
    f = open('ssid.txt', 'r')
    ssid = f.read()
    print(ssid)
    f.close()

  if 'pwd.txt' in os.listdir():
    f = open('pwd.txt', 'r')
    password = f.read()
    print(password)
    f.close()


  # --- Try to connect ---
  wlan = network.WLAN(network.STA_IF)

  wlan.active(True)
  wlan.connect(ssid, password)

  wait_time = time.ticks_ms() + 5000
  
  while wlan.isconnected() == False:
    if wait_time < time.ticks_ms():
      f = open('state.txt', 'w')
      f.write('START_STATE')
      f.close()
      machine.reset()
      break

  print('Connection successful')
  print(wlan.ifconfig())
  monitoring_state.monitor_state()
 
