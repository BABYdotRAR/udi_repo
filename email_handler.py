import smtplib
from email.message import EmailMessage
import ssl
import env_variables as env

sender_email = env.EMAIL_SENDER
sender_password = env.EMAIL_APP_PASSWORD
subject = 'Código QR UDI ESIT'
body = """
    𝐻𝑜𝓁𝒶, 𝒶𝓆𝓊í 𝓉𝒾𝑒𝓃𝑒𝓈 𝓉𝓊 𝒸ó𝒹𝒾𝑔𝑜 𝒬𝑅 𝒸𝑜𝓃 𝑒𝓁 𝓆𝓊𝑒 𝓅𝑜𝒹𝓇á𝓈 𝓅𝑒𝒹𝒾𝓇 𝓅𝓇é𝓈𝓉𝒶𝓂𝑜 𝒹𝑒 𝑒𝓆𝓊𝒾𝓅𝑜 𝑒𝓃 𝓁𝒶 𝒰𝒟𝐼 ☺
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
    smtp_server = 'smtp.gmail.com'  # Update this with your SMTP server
    smtp_port = 465#587  # Update this with your SMTP port
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            #server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            return "OK"
    except Exception as e:
        return f'An error occurred while sending the email: {str(e)}'
