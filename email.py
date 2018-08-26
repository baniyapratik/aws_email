import boto3
from botocore.exceptions import ClientError
import logging
from jinja2 import Environment, FileSystemLoader
file_loader = FileSystemLoader('templates')

log = logging
email_tmp_env = Environment(loader=file_loader)

class Email:
    def __init__(self, RECIPIENT=None, SUBJECT='', BODY_TEXT='', BODY_HTML='', SENDER='admin@cafy.io', CHARSET='UTF-8', region_name='us-east-1'):
        self.SENDER = SENDER
        self.RECIPIENT = RECIPIENT# This could be one person or a list
        self.SUBJECT = SUBJECT
        self.BODY_TEXT = BODY_TEXT
        self.BODY_HTML = BODY_HTML
        self.CHARSET = CHARSET
        self.client = boto3.client('ses', region_name) #default region for ses service

    def send_email(self):
        '''
        This service is responsible for sending emails
        
        :return: None
        '''
        try:
            # Provide the contents of the email.
            response = self.client.send_email(
                Destination={
                    'ToAddresses': [
                        self.RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': self.CHARSET,
                            'Data': self.BODY_HTML,
                        },
                        'Text': {
                            'Charset': self.CHARSET,
                            'Data': self.BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': self.CHARSET,
                        'Data': self.SUBJECT,
                    },
                },
                Source=self.SENDER,

            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])

    def send_welcome_mailer(self, person):
        template = email_tmp_env.get_template('welcome.html')
        self.RECIPIENT = person['email']
        self.BODY_HTML = template.render(firstName=person['firstName'])
        self.SUBJECT = 'Welcome to Cafy'
        self.send_email()

if __name__ == '__main__':
    person = {}
    person['firstName'] = "Pratik"
    person['email'] = 'prabaniy@cisco.com'
    email = Email()
    email.send_welcome_mailer(person)
