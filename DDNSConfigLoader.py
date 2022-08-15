
from mailSMTP import mailSMTP
from cloudflareAPIDNS import cloudflareAPIDNS

## A class designed to read a config file and init required objects


##A function designed to scan a config file looking for a variable name and return the value
# @param filename The config filename (String)
# @param variableName The vairable name in the config file (String)
# @throws configError Error reading configuration
def getVariableFromConfig(filename, variableName):
    #Open config file
    configFile = open(filename, "r")
    config = configFile.readlines()
    #Loop through each line
    for configLine in config:
        #Remove trailing whitespace
        configLine = configLine.strip()
        #Check if empty line
        if len(configLine) > 0:
            #Check if comment line
            if configLine[0] != "#":
                #Remove spaqces
                configLine = configLine.replace(" ", "")
                #Split to two variables
                lineVar, lineVal = configLine.split("=", 1)
                #Check if var specified in line is wanted var
                if lineVar.lower() == variableName.lower():
                    return lineVal
    #If not found raise error
    raise configError()

##Create cloudflare object from config file
# @param filename Filename of config file
# @returns Initalised Cloudflare DNS Object 

def loadCloudflareObject(filename):
    #Get required vairables
    authToken = getVariableFromConfig(filename, "authToken")
    zoneID = getVariableFromConfig(filename, "zoneID")
    #Create object
    cloudflareDNSObject = cloudflareAPIDNS(authToken, zoneID)
    return cloudflareDNSObject

## Get and format domain variables from config file
# @param filename Filename of config file
# @throws configError Error reading configuration
# @returns List of domains [String], Blacklist? (Bool), IPv4? (Bool)
def loadDomainConfig(filename):
    #Get required variables
    domainListString = getVariableFromConfig(filename, "list")
    blacklistString = getVariableFromConfig(filename, "list")
    IPv4String = getVariableFromConfig(filename, "IPv4")

    #Convert to required format with default backup
    try:
        if domainListString.lower() == "none":
            domainList = []
        else:
            domainList = domainListString.split(",")
    except:
        raise configError
    if blacklistString.lower() == "false":
        blacklist = False
    else:
        blacklist = True

    if IPv4String.lower() == "false":
        IPv4 = False
    else:
        IPv4 = True
    
    return domainList, blacklist, IPv4

## Create mailSMTP object from config file
# @param filename Filename of config file
# @throws configError Error reading configuration
# @returns mailSMTPObjectr
def loadSMTPObject(filename):
    #Get variables from config
    key = getVariableFromConfig(filename, "key")
    secret = getVariableFromConfig(filename, "secret")
    server = getVariableFromConfig(filename, "server")
    portString = getVariableFromConfig(filename, "port")
    TLSString = getVariableFromConfig(filename, "TLS")
    recAddress = getVariableFromConfig(filename, "recAddress")
    sendAddress = getVariableFromConfig(filename, "sendAddress")
    
    #Convert type as required
    try:
        port = int(portString)
    except:
        raise configError()
    
    #Default to true for security
    if TLSString.lower() == "false":
        TLS = False
    else:
        TLS = True

    mailSMTPObject = mailSMTP(key, secret, server, port, sendAddress, recAddress, TLS)
    return mailSMTPObject


    


class configError(Exception):
    pass

