virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
apt install ansible
apt install vagrant
ansible-galaxy collection install community.windows
ansible-galaxy collection install community.general
vagrant plugin install vagrant-vbguest
vagrant plugin install vagrant-scp

