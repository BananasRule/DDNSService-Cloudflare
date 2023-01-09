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
    #Attempt to get IP upto 30 times from both primary and fallback services if unsuccessful
    #Will immediatly return if ip address was sucessfuly obtained from either source
    attemptCounter = 0
    while attemptCounter <= 30:
        try:
            ipAddressResponce = getIPPrimary()
            if ipAddressResponce.status_code != 200:
                raise getIPError()
            else:
                #This is not the best way of doing this, but as it is a short and
                #simple function this is still readable and maybe more so then 
                #other approches 
                return ipAddressResponce.text
        except:
            try:
                ipAddressResponce = getIPFallback()
                if ipAddressResponce.status_code != 200:
                    raise getIPError()
                else:
                    return ipAddressResponce.text
            except:
                attemptCounter = attemptCounter + 1
        
#Define IP services
def getIPFallback():
    ipAddressResponce = requests.get("https://api.ipify.org/")
    return ipAddressResponce

def getIPPrimary():
    ipAddressResponce = requests.get("https://ip.seeip.org")
    return ipAddressResponce


class getIPError(Exception):
    pass
        