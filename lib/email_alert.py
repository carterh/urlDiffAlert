import smtplib

default_sender = 'alerts@henrycarter.org'
default_subject = 'URL diff alert'
default_smtp_server = 'mta5.am0.yahoodns.net'

#This function defaults to yahoo's smtp server, so recipients must be yahoo addresses
def send_alert(body, recipients, subject=default_subject, smtp_server=default_smtp_server):
    message_components = ['From: ' +  default_sender, 'To: ' + ', '.join(recipients), 'Subject: ' + subject, '', body]
    message = '\r\n'.join(message_components)
    
    #TO-DO: SMTP_SSL times out for this SMTP server
    with smtplib.SMTP(smtp_server) as server:
        server.starttls()
        server.sendmail(default_sender, recipients, message)
