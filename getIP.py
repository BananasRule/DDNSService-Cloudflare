
import requests, time     
#Requests
#Copyright 2019 Kenneth Reitz

## Get IP address from Ipify and check the response was ok
# @throws getIPError Cannot connect to server / Invalid responce 
# @returns Current IP Address (String)
def getIP():
    try:
        ipAddressResponce = requests.get("https://api.ipify.org/")
        currentIPAddress = ipAddressResponce.text
    except:
        time.sleep(30)
        try:
            ipAddressResponce = requests.get("https://api.ipify.org/")
            currentIPAddress = ipAddressResponce.text
        except:
            raise getIPError()
    if ipAddressResponce.status_code != 200:
        raise getIPError()
    return currentIPAddress

class getIPError(Exception):
    pass
        