#! /bin/bash

while :
do
CN=`iwgetid -r` #gets currently connected network name
SN="ARRIS-CD12" #replace with basestation access point name
  if [ "$CN" == "$SN" ];
  then
	iwconfig wlan0 | grep "Signal level" > signal.txt #saves signal strength/quality to file 
        stty 9600 -F /dev/serial1 raw -echo #starts serial terminal, change serial1 to correct port
        cat signal.txt >/dev/serial1 #sends data to arduino, change serial1 to correct port
     	sleep 2 #waits 2 seconds
  fi
done
