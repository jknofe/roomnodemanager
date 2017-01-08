#!/usr/bin/python
# -*- coding: utf-8 -*-
import serial
import sys
import os
import signal
import time

# known devices, configure ID, name and script to process data
NodesDict = {
				'05':	["RoomNode5",	"python /home/pi/git/roomnodemanager/rntemp2fhem.py" , 0],
				'14':	["BattMon RX8",	"perl /home/pi/git/battmon/read_battery.pl"			, 0]
			}


# end script and close serial device on SIGINT
def _EndRoomNodeManager(signum, frame):
    ser.close()
    if(ser.isOpen()):
    	print("ERROR - Serial " + str(ser.port) + " was not closed.")
    	sys.exit(1)
    else:
    	sys.exit(0)

# register _EndRoomNodeManager for SIGINT ( Ctrl+C ) and SIGTERM ( kill $PID )
signal.signal(signal.SIGINT,  _EndRoomNodeManager)
signal.signal(signal.SIGTERM, _EndRoomNodeManager)

# configure serial device
ser = serial.Serial()
ser.baudrate = 38400		# speed
ser.port = '/dev/ttyUSB0'	# device
#ser.timeout = 3600 			# s


# open serial device
ser.open()

# do the endless loop
while(ser.isOpen()):
	# read one line from serial
	line = ser.readline()
	
	# get node ID
	NodeID = line[2:4]

	# check if node is in dict and push data to script
	if NodeID in NodesDict:
		# calc delta since last ID received
		timestamp  = int(time.time())
		deltaT =  timestamp - NodesDict[NodeID][2]
		NodesDict[NodeID][2] = timestamp
		#
		print("ID: " + str(NodeID) + " - dt: " + str(deltaT) + "s")
		sh_command = NodesDict[NodeID][1] + " " + line
		#
		#print(line)
		os.system(sh_command)
	else:
		print("WARNING - Node ID: " + NodeID + " received but not configured in dictionary")

# we schould never reach this line in normal operation
print("Serial " + str(ser.port) + " was closed. ")

# EOF
