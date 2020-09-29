import smtplib

default_sender = 'alerts@henrycarter.org'
default_smtp_server = 'mta5.am0.yahoodns.net'

#This function defaults to yahoo's smtp server, so recipients must be yahoo addresses
def send_alert(body, recipients, subject, sender=default_sender, smtp_server=default_smtp_server):
    message_components = ['From: ' +  sender, 'To: ' + ', '.join(recipients), 'Subject: ' + subject,'Content-Type: ' + 'text/html; charset=utf-8','', body]
    message = '\r\n'.join(message_components)
    
    #TO-DO: SMTP_SSL times out for this SMTP server
    with smtplib.SMTP(smtp_server) as server:
        server.starttls()
        server.sendmail(sender, recipients, message.encode())
