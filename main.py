try:
  import usocket as socket
except:
  import socket

import machine
import onewire
import network
import ds18x20
import start_state
import monitoring_state
import os

from time import sleep_ms, ticks_ms
from machine import I2C, Pin
from machine_i2c_lcd import I2cLcd

state = 'MONITOR_STATE'
ssid = 'NONE'
password = 'NONE'
DEFAULT_I2C_ADDR = 0x27


try:
  ow = onewire.OneWire(Pin(12))
  ds = ds18x20.DS18X20(ow)
  roms = ds.scan()
  ds.convert_temp()
  sleep_ms(750)
  for rom in roms:
    print(ds.read_temp(rom))
except:
  ds = "ERROR"

  
i2c = I2C(1, freq=100000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)
lcd.putstr(" Checking  Wifi ")
sleep_ms(2000)
lcd.clear()

# --- Check State ---
if 'state.txt' in os.listdir():
  f = open('state.txt', 'r')
  state = f.read()
  print(state)
  f.close()
else:
  state = 'START_STATE'

if state == 'START_STATE':
  print('Not connected - Start procedure')
  # Must have: Temperature, ON/OFF button, ssid/pwd
  wlan = network.WLAN(network.AP_IF) # create access-point interface
  wlan.config(ssid='AQUA') # set the SSID of the access point
  wlan.config(max_clients=10) # set how many clients can connect to the network
  wlan.active(True)         # activate the interface

  tmp_ip_address = wlan.ifconfig()
  ip_address = str(tmp_ip_address[0])

  start_state.start_state(lcd, ip_address, ds)

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

  wait_time = ticks_ms() + 10000
  
  while wlan.isconnected() == False:
    if wait_time < ticks_ms():
      f = open('state.txt', 'w')
      f.write('START_STATE')
      f.close()
      machine.reset()
      break

  print('Connection successful')
  tmp_ip_address = wlan.ifconfig()
  ip_address = str(tmp_ip_address[0])

  monitoring_state.monitor_state(lcd, ip_address, ds)
 
