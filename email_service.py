# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage


def send_msg_to_clinet(data_to_send, email_id_requested):
    msg = EmailMessage()
    msg.set_content(data_to_send)
    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = 'Top 10 restaurants'
    msg['From'] = "cirilla2510@gmail.com"
    msg['To'] = email_id_requested

    # Send the message via our own SMTP server.
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    s.login('cirilla2510@gmail.com', 'Dry69oh@mb')
    s.send_message(msg)
    s.quit()
