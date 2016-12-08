#!/usr/bin/python3
# file: sendEmail.py
# Eilidh Southren - 1513195


#-----------------------------------------
#
#   This script sends an email to the user
#   if they have supplied authorisation
#   credentials in a text file. 
#
#

import smtplib
import email.utils
from email.message import Message
import getpass
import time
import os.path


def sendEmail():

    currentTime = time.strftime("%d/%m/%y - %H:%M:%S")

    #   if email credentials have been supplied, read email
    #   credentials file and set authentication/server variables

    if os.path.isfile('email_credentials.txt'):
        
        file = open('email_credentials.txt', 'r')
        
        lines = file.readlines()

        to_email = lines[0]
        servername = lines[1]
        username = lines[2].rstrip('\n')
        password = lines[3].rstrip('\n')
        from_sender_name = lines[4]
        from_sender_email = lines[5]

        body = '''The RasProtect Alarm System was triggered on ''' + currentTime

        subject = 'RasProtect System'

        msg = Message()
        msg['To'] = email.utils.formataddr(('Recipient', to_email))
        msg['From'] = email.utils.formataddr((from_sender_name, from_sender_email))
        msg['Subject'] = subject
        msg['Date'] = email.utils.formatdate(localtime = 1)
        msg['Message-ID'] = email.utils.make_msgid()
        msg.set_payload(body)

        server = smtplib.SMTP(servername)

        try:
            # for verbose reporting
            server.set_debuglevel(True)

            # identify ourselves, prompting server for supported features
            server.ehlo_or_helo_if_needed()

            # If we can encrypt this session, do it
            if server.has_extn('STARTTLS'):
                server.starttls()
                # re-identify ourselves over TLS connection
                server.ehlo_or_helo_if_needed() 

            server.login(username, password)
            
            server.send_message(msg)
        finally:
            server.quit()

    else:
        print("Email Credentials have not been supplied, email notification not sent.")
