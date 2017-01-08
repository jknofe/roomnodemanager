#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os

# set fhem reading
def FhemSetReading(fhem_Device, fhem_Reading, fhem_Value):
	import urllib2

	# set fhem command
	fhem_http_cmd = "http://127.0.0.1:8083/fhem?cmd=set%20" + fhem_Device + "%20" + fhem_Reading + "%20" + fhem_Value

	#print(fhem_http_cmd)
	ret = urllib2.urlopen(fhem_http_cmd).read()

	return True

if(len(sys.argv) == 2):

	line = str(sys.argv[1])
	# debug output
	print(line.upper())
	# calc the value from bytes received
	rnid = line[2:4]
	
	temp_byte_lo = int(line[20:22], 16)
	temp_byte_hi = int(line[22:24], 16)
	#print(line[22:24] + "  " + line[20:22])
	if temp_byte_hi > 16:
		offset = 6553.5
	else:
		offset = 0

	temp = float( ((256  * temp_byte_hi) + temp_byte_lo ) - offset) / 10	
	humi = float(   256  * int(line[16:18], 16) + int(line[14:16], 16 ) ) / 10
	rssi = float( ( -1  * int(line[26:28], 16)) / 2)
	# debug output
	print("T: " + str(temp) + '°C | H: ' + str(humi) + "% | rssi: " + str(rssi) + "db" )
	# push value to fhem
	FhemDevName = "TempHum_" + rnid
	FhemSetReading(FhemDevName, 'T',    str(temp))
	FhemSetReading(FhemDevName, 'H',    str(humi))
	FhemSetReading(FhemDevName, 'rssi', str(rssi))
else:
	pass

#EOF
