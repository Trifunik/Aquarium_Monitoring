
try:
  import usocket as socket
except:
  import socket

import monitor_web_page
from machine import Pin
import re

light_pin = Pin(12, Pin.OUT)


light_state = "OFF"

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

  while True:

    if light_pin.value() == 1:
      light_state="ON"
    else:
      light_state="OFF"

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
    if light_off == 6:
      print('LED OFF')
      light_pin.value(0)

    wlan_data = request.split("HTTP/",1)

    response = monitor_web_page.web_page(light_state)

  

    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
