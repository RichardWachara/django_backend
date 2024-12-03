#import the django built in function to send emails using the configured backends
# from django.core.mail import send_mail - used to send simple emails with a message

# To send html email templates we use the following
from django.core.mail import EmailMultiAlternatives

# use the thread library in python to create a different thread to handle sending emails - faster application
import threading 


# create a separete thread to handle sending emails
class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, from_email,recipient_list):
        self.subject = subject
        self.html_content =html_content
        self.from_email = from_email
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)
    
    # define a method that will be executed once the thread is started using the start()
    def run(self):
        msg = EmailMultiAlternatives(
            self.subject,
            '',
            self.from_email,
            self.recipient_list
        )
        msg.attach_alternative(self.html_content, 'text/html')
        msg.send()

        

# create an abstraction to create and run the thread using the required data
def send_email_async(subject,html_content,from_email,recipient_list):
    EmailThread(subject,html_content,from_email,recipient_list).start()

def send_registration_email(user_email, first_name,verification_url):
    subject = "Welcome To our Platfrom"
    html_content = f"""
    <!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
        }}
        .header {{
            background-color: #f4f4f4;
            padding: 20px;
            text-align: center;
        }}
        .content {{
            margin: 20px;
        }}
        .footer {{
            background-color: #f4f4f4;
            text-align: center;
            font-size: 12px;
            color: #888;
            margin-top: 30px;
            padding: 10px;
        }}
        .button {{
            display: inline-block;
            padding: 10px 20px;
            margin-top: 20px;
            font-size: 16px;
            color: #ffffff;
            background-color: #007BFF;
            text-decoration: none;
            border-radius: 5px;
        }}
        .button:hover {{
            background-color: #0056b3;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Welcome, {first_name}!</h1>
    </div>
    <div class="content">
        <p>Hi {first_name},</p>
        <p>Thank you for registering with us. We're excited to have you on board!</p>
        <p>If you have any questions, feel free to reply to this email.</p>
        <a href="{verification_url}" class="button">Verify Your Account</a>
    </div>
    <div class="footer">
        &copy; 2024 My App. All rights reserved.
    </div>
</body>
</html>
    """
    from_email = 'MY APP'
    recipient_list = [user_email]

    send_email_async(subject,html_content,from_email,recipient_list)