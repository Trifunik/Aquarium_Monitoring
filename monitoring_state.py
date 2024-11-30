
try:
  import usocket as socket
except:
  import socket

import monitor_web_page
from machine import Pin
import re

light_pin = Pin(12, Pin.OUT)

# set default on an off time
# 
def monitor_state():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('', 80))
  s.listen(5)

  HOUR_ON = "09"
  MIN_ON = "00"
  HOUR_OFF = "18"
  MIN_OFF = "00"

  next_state = "ON"

  while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    light_on = request.find('/?light=on')
    light_off = request.find('/?light=off')

    if light_on == 6:
      print('LED ON')
      light_pin.value(1)
      next_state="OFF"
    if light_off == 6:
      print('LED OFF')
      light_pin.value(0)
      next_state="ON"

    # Get ON/OFF Time
    wlan_data = request.split("HTTP/",1)
    result = re.search('onTime=(.*)&', wlan_data[0])
    if result is not None:
      print(result.group(1))
      tmp = result.group(1)
      tmp_array = tmp.split("%3A")
      HOUR_ON = tmp_array[0]
      MIN_ON = tmp_array[1]
    
    result = re.search('offTime=(.*) ', wlan_data[0])
    if result is not None:
      print(result.group(1))
      tmp = result.group(1)
      tmp_array = tmp.split("%3A")
      HOUR_OFF = tmp_array[0]
      MIN_OFF = tmp_array[1]

    response = monitor_web_page.web_page(next_state,HOUR_ON,MIN_ON,HOUR_OFF,MIN_OFF)

  

    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
