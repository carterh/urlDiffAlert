import smtplib

def send_alert(body, recipients, subject, sender, smtp_server):
    message_components = ['From: ' +  sender, 'To: ' + ', '.join(recipients), 'Subject: ' + subject,'Content-Type: ' + 'text/html; charset=utf-8','', body]
    message = '\r\n'.join(message_components)
    
    #TO-DO: SMTP_SSL times out for some SMTP servers
    with smtplib.SMTP(smtp_server) as server:
        server.starttls()
        server.sendmail(sender, recipients, message.encode())
