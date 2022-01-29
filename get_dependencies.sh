#!/bin/bash
sudo apt update 
sudo apt install -y python3-dev linux-headers-generic python3-pip python3-virtualenv
sudo apt install -y ansible vagrant virtualbox virtualbox-dkms unzip git
sudo gem install winrm-elevated
sudo gem install winrm
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ansible-galaxy collection install community.windows
ansible-galaxy collection install community.general
vagrant plugin install vagrant-vbguest
vagrant plugin install vagrant-scp

