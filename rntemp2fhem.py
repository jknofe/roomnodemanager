#!/usr/bin/python
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


#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

if(len(sys.argv) == 2):
	line = str(sys.argv[1]);

	temp = float(256*int(line[22:24], 16) + int(line[20:22], 16 ) ) / 10
	humi = float(256*int(line[16:18], 16) + int(line[14:16], 16 ) ) / 10
	print(temp)
	print(humi)

	FhemSetReading('TempHum_05', 'T', str(temp))
else:
	pass

#temp = ((float)((int16_t)((uint16_t)buf[10]<<8 | buf[9]))/10);
#humi = (float)((float)(buf[7]*256 + buf[6])/10);
#batt = (uint16_t)((1100UL*1024UL)/(buf[5]*256+buf[4]));

#FhemSetReading('TempHum_05', 'T', str(temp))
#FhemSetReading('TempHum_05', 'H', str(humi))


#EOF
