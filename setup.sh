#!/usr/bin/env bash

# Install stuff
sudo apt install -y python3-pip python3-rpi.gpio python3-pygame vim git

# Checkout the code
cd ~
git clone https://github.com/mikeflynn/TheBatPhone.git batphone

sudo ln -s ~/batphone/ /opt/batphone

# Start scripts on boot
crontab -l | grep '/opt/batphone/batphone.py' 1>/dev/null 2>&1
if [[ $? == 1 ]]; then
	line="@reboot python3 /opt/batphone/batphone.py"
	(crontab -u $(whoami) -l; echo "$line" ) | crontab -u $(whoami) -
fi

# Add the following to /etc/rc.local for the shutdown functionality:
#
# sudo python3 /home/pi/batphone/shutdown.py


