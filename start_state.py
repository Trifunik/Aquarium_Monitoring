try:
  import usocket as socket
except:
  import socket

import start_web_page
import machine
import re

def start_state():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    ssid_check = False
    pwd_check = False

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)
        print('Content = %s' % request)

        wlan_data = request.split("HTTP/",1)

        # Get SSID and save in ssid file
        result = re.search('ssid=(.*)&', wlan_data[0])
        if result is not None:
            f = open('ssid.txt', 'w')
            f.write(result.group(1))
            f.close()
            ssid_check = True
        
        result = re.search('pwd=(.*) ', wlan_data[0])
        if result is not None:
            f = open('pwd.txt', 'w')
            f.write(result.group(1))
            f.close()
            pwd_check = True

        if ssid_check == True and pwd_check == True:
          f = open('state.txt', 'w')
          f.write('MONITOR_STATE')
          f.close()
          machine.reset()

        response = start_web_page.web_page()

        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
