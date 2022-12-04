##© Jacob Gray 2022
##This Source Code Form is subject to the terms of the Mozilla Public
##License, v. 2.0. If a copy of the MPL was not distributed with this
##file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests, time     
#Requests
#Copyright 2019 Kenneth Reitz

## Get IP address from Ipify and check the response was ok
# @throws getIPError Cannot connect to server / Invalid responce 
# @returns Current IP Address (String)
def getIP():
    try:
        ipAddressResponce = getIPPrimary()
    except:
        time.sleep(30)
        try:
            ipAddressResponce = getIPFallback()
        except:
            raise getIPError()
    if ipAddressResponce.status_code != 200:
        raise getIPError()
    return ipAddressResponce.text

def getIPPrimary():
    ipAddressResponce = requests.get("https://api.ipify.org/")
    return ipAddressResponce

def getIPFallback():
    ipAddressResponce = requests.get("https://ip.seeip.org")
    return ipAddressResponce


class getIPError(Exception):
    pass
        