# Email Dependencies
import smtplib
from email.mime.text import MIMEText

class Email():

    def __init__(self):
        print "Creating Email instance!"

    def send_low_coffee_email(self):
        print "Sending coffee is low email"

        msg = MIMEText("KEN REFILL THE COFFEE ITS LOW!")
        msg['Subject'] = 'The Coffee Is Low: Refill It!'
        msg['From'] = 'coffee@makeandbuild.com'
        msg['To'] = 'ken.orji@makeandbuild.com'

        # Send the message
        s = smtplib.SMTP('localhost')
        s.sendmail('jeremy.dyer@makeandbuild.com', 'ken.orji@makeandbuild.com', msg.as_string())
        s.quit()