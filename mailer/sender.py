import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header
from dotenv import load_dotenv

load_dotenv()

def send_email(subject, content):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    receiver = os.getenv("EMAIL_TO")

    msg = MIMEText(content, "plain", "utf-8")
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = Header(subject, "utf-8")

    smtp = smtplib.SMTP_SSL("smtp.163.com", 465)
    smtp.login(sender, password)
    smtp.sendmail(sender, [receiver], msg.as_string())
    smtp.quit()

    print("邮件发送成功")