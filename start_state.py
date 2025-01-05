try:
  import usocket as socket
except:
  import socket

from time import sleep_ms
import start_web_page
import machine
import re
import ds18x20

light_pin = machine.Pin(16, machine.Pin.OUT)

global_dict = {
  "IP_ADDRESS": "10.10.10.10",
  "next_state": "ON",
  "temp": "00.0"
}

def get_temp(ds):
  global global_dict
  
  roms = ds.scan()
  ds.convert_temp()
  sleep_ms(750)
  for rom in roms:
    temp = str(ds.read_temp(rom))

  global_dict["temp"] = temp[:4]+"C"


def periodic_func(lcd,ds):
  global global_dict

  get_temp(ds)
  lcd.move_to(6,0)
  lcd.putstr(global_dict["temp"])

def set_light(light_on, light_off):
	global global_dict

	if light_on == 6:
		light_pin.value(1)
		global_dict["next_state"]="OFF"
	
	if light_off == 6:
		light_pin.value(0)
		global_dict["next_state"]="ON"

  
def start_state(lcd, ip_address, ds):
  global global_dict

  global_dict["IP_ADDRESS"] = ip_address

  lcd.putstr("Start State")
  sleep_ms(1000)
  lcd.clear()

  lcd.move_to(2,1)
  lcd.putstr(ip_address)

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('', 80))
  s.listen(5)

  if type(ds) != str:
    timer = machine.Timer(0)
    timer.init(period=4000, mode=machine.Timer.PERIODIC, callback=lambda b: periodic_func(lcd, ds))

  ssid_check = False
  pwd_check = False

  while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)

    light_on = request.find('/?light=on')
    light_off = request.find('/?light=off')
    set_light(light_on, light_off)

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

    response = start_web_page.web_page(global_dict)

    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
