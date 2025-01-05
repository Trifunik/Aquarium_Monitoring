
try:
	import usocket as socket
except:
	import socket

from time import sleep_ms, localtime
import monitor_web_page
from machine import Pin, Timer
import re

import ntptime
import ds18x20

light_pin = Pin(16, Pin.OUT)

global_dict = {
	"IP_ADDRESS": "10.10.10.10",
	"HOUR_ON": "09",
	"MIN_ON": "00",
	"HOUR_OFF": "18",
	"MIN_OFF": "00",
	"on_time": 9.0,
	"off_time":18.0,
	"next_state": "ON",
	"light_state": "AUTOMATIC",
	"temp": "00.0"
}

def get_temp(ds):
	if type(ds) != str:
		global global_dict

		roms = ds.scan()
		ds.convert_temp()
		sleep_ms(750)
		for rom in roms:
			temp = str(ds.read_temp(rom))

		global_dict["temp"] = temp[:4]+"C"


# Turn on/off the light. If light is turned on via Wifi, go into manual mode
def set_light(light_on, light_off, state):
	global global_dict

	if (global_dict["light_state"] == "MANUAL") and (state == "ON" or state == "OFF"):
		if global_dict["next_state"] != state:
			global_dict["light_state"] = "AUTOMATIC"
		else:
			state = "MANUAL"

	if light_on == 6 or state == "ON":
		light_pin.value(1)
		global_dict["next_state"]="OFF"
	
	if light_off == 6 or state == "OFF":
		light_pin.value(0)
		global_dict["next_state"]="ON"

	if light_on == 6 or light_off == 6:
		global_dict["light_state"] = "MANUAL"

def periodic_func(lcd,ds):
	global global_dict

	temp = localtime()
	time_string = '{:02d}'.format(temp[3]+1) + ":" + '{:02d}'.format(temp[4])
	time_decimal = float(temp[3])+ 1.0 + float(temp[4]) / 60
 
	if global_dict["on_time"] <= time_decimal and time_decimal <= global_dict["off_time"]:
		set_light(0, 0, "ON")
	else:
		set_light(0, 0, "OFF")
	
	get_temp(ds)

	lcd.move_to(0,0)
	lcd.putstr(time_string)
	lcd.move_to(10,0)
	lcd.putstr(global_dict["temp"])
	lcd.move_to(0,1)
	lcd.putstr(global_dict["IP_ADDRESS"])

# set default on an off time
# 
def monitor_state(lcd, ip_address, ds):
	global global_dict

	global_dict["IP_ADDRESS"] = ip_address

	lcd.putstr("Monitoring State")
	sleep_ms(1000)
	lcd.clear()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('', 80))
	s.listen(5)
	ntptime.settime()

	get_temp(ds)

	timer = Timer(0)
	timer.init(period=4000, mode=Timer.PERIODIC, callback=lambda b: periodic_func(lcd, ds))

	while True:
		conn, addr = s.accept()
		print('Got a connection from %s' % str(addr))
		request = conn.recv(1024)
		request = str(request)
		print('Content = %s' % request)
		light_on = request.find('/?light=on')
		light_off = request.find('/?light=off')

		set_light(light_on, light_off, "NOT_SET")

		# Get ON/OFF Time
		wlan_data = request.split("HTTP/",1)
		result = re.search('onTime=(.*)&', wlan_data[0])
		if result is not None:
			print(result.group(1))
			tmp = result.group(1)
			tmp_array = tmp.split("%3A")
			global_dict["HOUR_ON"] = tmp_array[0]
			global_dict["MIN_ON"] = tmp_array[1]
			global_dict["on_time"] = float(tmp_array[0]) + float(tmp_array[1]) / 60
		
		result = re.search('offTime=(.*) ', wlan_data[0])
		if result is not None:
			print(result.group(1))
			tmp = result.group(1)
			tmp_array = tmp.split("%3A")
			global_dict["HOUR_OFF"] = tmp_array[0]
			global_dict["MIN_OFF"] = tmp_array[1]
			global_dict["off_time"] = float(tmp_array[0]) + float(tmp_array[1]) / 60

		response = monitor_web_page.web_page(global_dict)

		conn.send('HTTP/1.1 200 OK\n')
		conn.send('Content-Type: text/html\n')
		conn.send('Connection: close\n\n')
		conn.sendall(response)
		conn.close()
