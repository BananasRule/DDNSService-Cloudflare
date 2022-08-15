from datetime import datetime
import hashlib
from mailSMTP import mailSMTP

## Create a message from a list of statuses and a list of objects affected by that status
# @param affectedList A 2D list of affected domains [status][objects] (2D Array)

# affectedList is set up like so
# |status|object1|object2|...
# 
# |good|domain.example|domain1.example
# |bad|doamin2.example
def createMessage(affectedList):
    #Returned string
    message = ""
    #Loop through statuses 
    for status in affectedList:
        #Extract status and add to message
        message = message + status[0] + "\n"
        #GHet each affected object for the status
        #Exclude first element as it is the status
        for object in status[1:]:
            #Add affected element to message
            message = message + "   >" + object +"\n"
    return message

## Send a email from a list of statuses while checking that a previous email was not sent with the same message
# @param mailObject A mailSTMP object that has been initalised (mailSTMP object)
# @param affectedList A 2D list of affected domains [status][objects] (2D Array)
# @param fullSuccess Indicator if there wer errors (Bool)
# @param previousMsgHash The hash returned by this function of the previous message (String)
# @param ipAddress The current IP address of the host (String)
# @returns The current message hash
def composeMessage(mailObject, affectedList, fullSuccess, previousMsgHash, ipAddress):
    message = createMessage(affectedList)
    message = message + "The current IP Address of the server is " + ipAddress
    # Get has of current message
    # If a fault is reoccouring and email will be sent once per hour due to the hash encoding
    currentMsgHash = hashlib.sha256(bytes(str(datetime.now().hour) + message, "utf-8")).hexdigest()
    if currentMsgHash != previousMsgHash:
        if fullSuccess == True:
            mailObject.sendMail("SUCCESS: DNS Records Successful Updated", message)
        else:
            mailObject.sendMail("FAILURE: DNS Records Update Had Error", message)
    return(currentMsgHash)