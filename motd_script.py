#!/usr/bin/python

import os
import sys
import time
import socket
import subprocess
import importlib
from subprocess import PIPE, Popen

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan

try:
	import pip
except ImportError:
	print(R + "python-pip not installed. Run \"sudo apt install python-pip\"" + W)
	sys.exit()


# Import netifaces. Install if not present
try:
        import netifaces
except ImportError:
	print(R + "netifaces not installed. Installing..." + W)
        try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "netifaces"])
                print(G + "netifaces installed!" + W)
		import netifaces
        except Exception, e:
                print(R + "Could not install netifaces: "  + str(e) + W)

# Import pyfiglet. Install if not present
try:
	from pyfiglet import Figlet
except ImportError:
	print(R + "pyfiglet not installed. Installing..." + W)
	try:
		subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "pyfiglet"])
		print(G + "pyfiglet installed!" + W)
		import pyfiglet
	except Exception, e:
		print(R + "Could not install pyfiglet: "  + str(e) + W)

interfaces = [['eth0', ''], ['wlan0', '']]

def displayInfo(hostname, interfaces_array, temp):

	custom_fig = Figlet(font='slant', width=2000)
	print(R + custom_fig.renderText(hostname) + W)
	#ascii_banner = pyfiglet.figlet_format(hostname)
	#print(R + ascii_banner + W)

	for i in interfaces_array:
		print(C + i[0] + ": " + str(i[1]) + W)
	print(C + "Hostname: " + str(hostname) + W)
	print(C + "CPU Temp: " + str(temp) + u"\N{DEGREE SIGN}C" + W)

#print ("This is a message from python")

# Get network information
hostname = socket.gethostname()

#if not ni:
#	ip_address = socket.gethostbyname(hostname)
#else:
for i in interfaces:
	netifaces.ifaddresses(i[0])
	i[1] = netifaces.ifaddresses(i[0])[netifaces.AF_INET][0]['addr']

# Get cpu temperature
process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
output, _error = process.communicate()
cpu_temp = float(output[output.index('=') + 1:output.rindex("'")])
displayInfo(hostname, interfaces, cpu_temp)
