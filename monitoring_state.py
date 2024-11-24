
import web_page
import re

# set default on an off time
# 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

HOUR_ON = "09"
MIN_ON = "00"
HOUR_OFF = "18"
MIN_OFF = "00"

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)

  wlan_data = request.split("HTTP/",1)

  result = re.search('ssid=(.*)&', wlan_data[0])

  if result is not None:
    print(result.group(1))
  
  result = re.search('&pwd=(.*) HTTP', wlan_data[0])

  if result is not None:
    print(result.group(1))


  response = start_web_page.web_page()

 

  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()
