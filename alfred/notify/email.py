#!/usr/bin/env python3
"""Email related stuffs"""
import smtplib

class Email():
    """Email class to send notifications"""
    def __init__(self, email, passwd):
        self.email = email
        self.passwd = passwd
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(self.email, self.passwd)


    def send_mail(self, email, title, body):
        """Send email"""
        self.server.sendmail(email, title, body)


    def __exit__(self, exc_type, exc_value, traceback):
        """destructor"""
        self.server.quit()
