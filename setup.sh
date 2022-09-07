##© Jacob Gray 2022
##This Source Code Form is subject to the terms of the Mozilla Public
##License, v. 2.0. If a copy of the MPL was not distributed with this
##file, You can obtain one at http://mozilla.org/MPL/2.0/.

##APT pre commands
apt update -y
##Install python3
apt install python3 python3-pip curl -y
##Install pip dependancies
pip install requests
##Create folders
cd /opt
mkdir DDNSService-Cloudflare
##Download files
curl -L https://github.com/BananasRule/DDNSService-Cloudflare/tarball/master | tar -xz -C DDNSService-Cloudflare --strip-components 1
##Add to crontab (from https://stackoverflow.com/questions/878600/how-to-create-a-cron-job-using-bash-automatically-without-the-interactive-editor)
crontab -l > tempcron
echo "* * * * * cd /opt/DDNSService-Cloudflare && python3 /opt/DDNSService-Cloudflare/DDNSService-Cloudflare.py" >> tempcron
crontab tempcron
rm tempcron
##Open config file
cd /opt/DDNSService-Cloudflare
cp exampleConfig.conf DDNSConfig.conf
nano DDNSConfig.conf