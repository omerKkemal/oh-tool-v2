import smtplib
from email.message import EmailMessage

from utility.setting import Setting


config = Setting()
config.setting_var()

def getlist(s):
    """
    Processes a list of SQLAlchemy model objects, extracting relevant string
    information and splitting the string into a structured list of values.

    Args:
        s (list): List of SQLAlchemy model instances (e.g., `Assessment` objects).

    Returns:
        list: A list of lists, where each sublist contains strings parsed from the object string representations.
    """
    _filter = [str(info)[1:-1].split(',') for info in s]  # Split the string by '-' and store it in a list
    print(_filter)
    return _filter

def sendEmail(subject,body,to):
    msg = EmailMessage()
    msg.add_alternative(body,subtype=config.EMAIL_TYPE)
    msg['Subject'] = subject
    msg['To'] = to
    msg['From'] = config.EMAIL

    with smtplib.SMTP(config.SMTP_LINK,config.SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(config.EMAIL,config.EMAIL_PASSWORD)

        smtp.send_message(msg)