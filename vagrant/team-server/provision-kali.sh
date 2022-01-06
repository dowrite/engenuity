#!/bin/bash

apt update

# Silence "Restart services during package upgrades without asking?" prompt
echo '* libraries/restart-without-asking boolean true' | sudo debconf-set-selections

# Install xrdp
sudo apt install -qy xrdp

cat <<EOF > /etc/polkit-1/localauthority.conf.d/02-allow-colord.conf
polkit.addRule(function(action, subject) {
 if ((action.id == "org.freedesktop.color-manager.create-device" ||
 action.id == "org.freedesktop.color-manager.create-profile" ||
 action.id == "org.freedesktop.color-manager.delete-device" ||
 action.id == "org.freedesktop.color-manager.delete-profile" ||
 action.id == "org.freedesktop.color-manager.modify-device" ||
 action.id == "org.freedesktop.color-manager.modify-profile") &&
 subject.isInGroup("{users}")) {
 return polkit.Result.YES;
 }
});
EOF

sudo systemctl enable xrdp

# Install nmapscan.pl
mkdir /opt/nmapscan
cd /opt/nmapscan
git clone https://github.com/tedsluis/nmap.git
cd /opt/nmapscan/nmap
wget -q https://cdnjs.cloudflare.com/ajax/libs/gojs/1.8.37/go.js

reboot