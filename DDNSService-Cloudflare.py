##A python program designed to update dns records on cloudflare when your IP address changes
## THIS APPLICATION IS NOT ENDORSED, SPONSORED OR ASSOCIATED WITH CLOUDFLARE
## THIS APPLICATION USES THE CLOUDFLARE API V4

from datetime import datetime

import mailSend
import getIP
import DDNSConfigLoader
import cloudflareAPIDNS
import os.path

#Variables used in program
configFilename = "DDNSConfig.conf"
updateSuccess = False

##Define Logging system
def errorLog(message):
    logfile = open("DDNSLog.log", "a")
    logfile.write(str(datetime.now()) + " | " + message + "\n")
    logfile.close()

#Check if program data file exists and load data if it does
if os.path.exists("DDNS.data") == True:
    try:
        dataFile = open("DDNS.data", "r")
        previousIP, previousMessageHash, previousSuccess, previousRunHour = (dataFile.readline()).split(",")
        dataFile.close
    except:
        #If it fails to load create a placeholder
        previousIP, previousMessageHash, previousSuccess, previousRunHour = "0", "0", "False", "25"
else:
    #If not create placeholder
    previousIP, previousMessageHash, previousSuccess, previousRunHour = "0", "0", "False", "25"

currentMsgHash = previousMessageHash

#Attempt to get current IP Address
try:
    currentIP = getIP.getIP()
except:
    #In case of failure attempt to send an email and then exit
    errorLog("An error occourred when getting current IP Address")
    try:
        mail = DDNSConfigLoader.loadSMTPObject(configFilename)
        currentMsgHash = mailSend.composeMessage(mail, [["An error occured getting the IP address", "All records"]], False, previousMessageHash, "Unable to determine")
    except:
        pass
    exit()


#Check if current IP is the same as previous full success IP
if currentIP != previousIP or previousSuccess.lower() == "false" or str(datetime.now().hour) != previousRunHour:
    
    #Try to open config files
    try:
        cfAPI = DDNSConfigLoader.loadCloudflareObject(configFilename)
        mail = DDNSConfigLoader.loadSMTPObject(configFilename)
        domainList, blacklist, IPv4 = DDNSConfigLoader.loadDomainConfig(configFilename)
    except:
        #Create error log if problem occours
        #Can't send email due to lack of email data
        errorLog("An error occourred when reading config file, please check config")
        exit()
        

    #Attempt to update DNS records
    try:
        #Update DNS using cloudflare API
        status = cfAPI.updateRecords(currentIP, domainList, blacklist, IPv4)

        #Track if a change was made
        change = False
        #Successful domains
        if len(status[0]) != 0:
            change = True
            messageStatus = [["These domains were sucessfully updated"]]
            #Append each domain to the same list after the status message
            for domain in status[0]:
                messageStatus[len(messageStatus)-1].append(domain)

        #Check if failed domains
        if len(status[1]) == 0:
            updateSuccess = True
        else:
            #Added as error message
            change = True
            messageStatus.append(["These domains had an error updating"])
            for domain in status[1]:
                messageStatus[len(messageStatus)-1].append(domain)

        #Check if there were blacklisted domains
        if len(status[2]) != 0:
            change = True
            messageStatus.append(["These domains were not updated due to blacklist/whitelist policy"])
            for domain in status[2]:
                messageStatus[len(messageStatus)-1].append(domain)
        
        #Send email if changes were made
        if change == True:
            currentMsgHash = mailSend.composeMessage(mail, messageStatus, updateSuccess, previousMessageHash, currentIP)
            errorLog("Domains were altered and an email was sent")
        else:
            #If change not made log but don't send email
            errorLog("Domains not altered but their IP was checked")
    except:
        #If an error occours during updating domain or send email write to log and attempt to send email
        errorLog("An error occourred when updating records")
        currentMsgHash = mailSend.composeMessage(mail, [["An error occurred when updating the records", "All records"]], False, previousMessageHash, currentIP)
else:
    #If current IP address is the same as saved IP and the previous run was successful and the last run occoured within the hour log and exit
    #The hour part ensures that records are updated even if they are changed externally 
    updateSuccess = True
    errorLog("Host IP was same as stored IP, the previous run was successful and it occurred with in the same hour")
        
#Write data to file
dataFile = open("DDNS.data", "w")
dataFile.write(currentIP + "," + currentMsgHash + "," + str(updateSuccess) + "," + str(datetime.now().hour))
dataFile.close()
    
    

    

    

    
    


