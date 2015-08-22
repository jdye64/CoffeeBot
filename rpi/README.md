===Raspberry PI Coffee===

This segment of the project holds all of the code that will run on a raspberry pi device and separates that code
from the components that run in the crossbar server.

** Raspberry PI Installation **

```sudo apt-get update```
```sudo apt-get install python libusb-1.0-0 python-dev```
```mkvirutalenv coffee```
```pip install --pre pyusb```
```pip install autobahn```
```pip install requests```
```pip install twisted```
```git clone https://github.com/makeandbuild/coffee.git```
```cd ~/coffee```
```sudo python ./DymoUSBScaleReadingComponent.py```

##Running the Coffee iBeacon Scanner##
```sudo /home/pi/.virtualenvs/coffee/bin/python ~/coffee/rpi/iBeacon/iBeaconScannerComponent.py```
```sudo /home/pi/.virtualenvs/coffee/bin/python ~/coffee/rpi/scale/DymoUSBScaleReadingComponent.py```

## DaemonTools ##

Daemontools is used to monitor the running processes and relaunch them if they fail.

#Installation#
```sudo apt-get install daemontools daemontools-run```

A RPi device in the coffee environment can run 0-N services. For each component that you want to install you need
to run the following series of commands.

#Coffee Scale Component Installation#

Depends on the installation of daemontools outlined above

```sudo mkdir /etc/service/coffee-scale```
```sudo vi /etc/service/coffee-scale/run```
Paste the following contents into the file listed above
```
#!/bin/sh
sudo /home/pi/.virtualenvs/coffee/bin/python ~/coffee/rpi/scale/DymoUSBScaleReadingComponent.py
```

Make the script executable
```sudo chmod +x /etc/service/coffee-scale/run```