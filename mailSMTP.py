import smtplib
## A class designed to send mail via STMP simplifed from stmplib
class mailSMTP:
    ##Initalise class
    # @param key API Key / Username (String)
    # @param secret API Secret / Password (String)
    # @param server Server web address (String)
    # @param port Server STMP port (Int)
    # @param sendAddress The address the message will be sent from (String)
    # @param recAddress The address the message will be sent to (String)
    # @param TLS Use TLS (Bool)
    def __init__(self, key, secret, server, port, sendAddress, recAddress, TLS):
        self.header='To:'+recAddress+'\n'+'From:' +sendAddress+'\n' #+'subject:testmail\n' -- add to later 
        self.key = key
        self.secret = secret
        self.server = server
        self.port = port
        self.sendAddress = sendAddress
        self.recAddress = recAddress
        self.TLS = TLS
    ## Send email using the class objects
    # @param self mailSTMP object
    # @param subject Email subject line (String)
    # @param message Email message (String)
    def sendMail(self, subject, message):
        #Initiate communication
        mailServer = smtplib.SMTP(self.server, self.port)
        mailServer.ehlo()
        #Use TLS if selected
        if self.TLS == True:
            mailServer.starttls()
            mailServer.ehlo()
        # Login to mail server
        mailServer.login(self.key, self.secret)
        # Create mail message
        mailMessage = self.header + 'subject:' + subject +'\n' + message
        # Send message
        mailServer.sendmail(self.sendAddress, self.recAddress, mailMessage)
        # Close connection
        mailServer.close()


