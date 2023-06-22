import smtplib
from email.message import EmailMessage
import ssl
import env_variables as env

sender_email = env.EMAIL_SENDER
sender_password = env.EMAIL_APP_PASSWORD
subject = 'Código QR UDI ESIT'
body = """
    H͓̽o͓̽l͓̽a͓̽,͓̽ ͓̽a͓̽q͓̽u͓̽í͓̽ ͓̽t͓̽i͓̽e͓̽n͓̽e͓̽s͓̽ ͓̽t͓̽u͓̽ ͓̽c͓̽ó͓̽d͓̽i͓̽g͓̽o͓̽ ͓̽Q͓̽R͓̽ ͓̽c͓̽o͓̽n͓̽ ͓̽e͓̽l͓̽ ͓̽q͓̽u͓̽e͓̽ ͓̽p͓̽o͓̽d͓̽r͓̽á͓̽s͓̽ ͓̽p͓̽e͓̽d͓̽i͓̽r͓̽ ͓̽p͓̽r͓̽é͓̽s͓̽t͓̽a͓̽m͓̽o͓̽s͓̽ ͓̽d͓̽e͓̽ ͓̽e͓̽q͓̽u͓̽i͓̽p͓̽o͓̽ ͓̽e͓̽n͓̽ ͓̽l͓̽a͓̽ ͓̽U͓̽D͓̽I͓̽
"""

def send_email_with_image(receiver_email, image_path):
    # Create a new email message
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(body)

    # Load the image file
    with open(image_path, 'rb') as f:
        image_data = f.read()

    # Add the image as an attachment
    msg.add_attachment(image_data, maintype='image', subtype='jpg', filename='image.jpg')

    # Set up the SMTP server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
            return "OK"
    except Exception as e:
        return f'An error occurred while sending the email: {str(e)}'
    
