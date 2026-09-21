import barcode
from barcode.writer import ImageWriter
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def generate_barcode(data, file_name):
    barcode_type = barcode.get_barcode_class('code128')
    my_barcode = barcode_type(data, writer=ImageWriter())
    file_path = my_barcode.save(file_name)
    return file_path

def send_email_with_barcode(to_email, barcode_file):
    from_email = "madarapurushyashrungan@gmail.com"
    from_password = "hwzs kyos pphr sabo"
    subject = "Your Generated Barcode"
    body = "Your barcode has been generated and attached."

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with open(barcode_file, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(barcode_file)}")
    msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_alert_email(registed_email):
    from_email = "madarapurushyashrungan@gmail.com"
    from_password = "hwzs kyos pphr sabo"
    subject = "Unauthorized Access Alert"
    body = "An unauthorized access attempt was detected in the system."

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)

        msg = EmailMessage()
        msg['From'] = from_email
        msg['To'] = registed_email
        msg['Subject'] = subject
        msg.set_content(body)
        server.send_message(msg)
        server.quit()
        print("Alert email sent.")
    except Exception as e:
        print(f"Failed to send alert email: {e}")


def send_otp_email(registed_email, otp):
    from_email = "madarapurushyashrungan@gmail.com"
    from_password = "hwzs kyos pphr sabo"
    subject = "Your OTP for Verification"
    body = f"Your OTP for verification is: {otp}"

    msg = EmailMessage()
    msg['From'] = from_email
    msg['To'] = registed_email="rushyashrungan05@gmail.com"
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
        server.quit()
        print(f"OTP sent to registed gmail {registed_email}")
        return True
    except Exception as e:
        print(f"Failed to send OTP: {e}")
        return False