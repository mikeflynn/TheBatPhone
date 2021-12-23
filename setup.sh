#!/usr/bin/env bash

# Install stuff
sudo apt -y install python3-pip python3-pygame vim git

# Checkout the code
cd /home/pi
git clone https://github.com/mikeflynn/TheBatPhone.git batphone 

# Start script on boot
crontab -l | grep '/home/pi/batphone/batphone.py' 1>/dev/null 2>&1
if [[ $? == 1 ]]; then
	line="@reboot python3 /home/pi/batphone/batphone.py"
	(crontab -u $(whoami) -l; echo "$line" ) | crontab -u $(whoami) -
fi