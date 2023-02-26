#file for sending the email
from django.core.mail import EmailMessage
class Util:
    @staticmethod
    def send_email(data):
        #use of email message class
        email=EmailMessage(subject=data['email_subject'],body=data['email_body'],to=(data['email_to'],))
        email.send()