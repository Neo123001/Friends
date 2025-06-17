import smtplib
from email.mime.text import MIMEText

def send_newsletter(emails, body):
    msg = MIMEText(body)
    msg["Subject"] = "Your Monthly Newsletter"
    msg["From"] = "you@example.com"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("you@example.com", "your_app_password")
        for to in emails:
            msg["To"] = to
            server.sendmail("you@example.com", to, msg.as_string())
