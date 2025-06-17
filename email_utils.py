import smtplib
from email.mime.text import MIMEText
import os

SENDER = os.getenv("NEWSLETTER_SENDER_EMAIL")
APP_PASSWORD = os.getenv("NEWSLETTER_APP_PASSWORD")

def send_newsletter_email(subject: str, content: str, recipients: list[str]):
    if not SENDER or not APP_PASSWORD:
        print("Missing email sender or password in env")
        return

    msg = MIMEText(content, "plain")
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = ", ".join(recipients)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER, APP_PASSWORD)
            server.sendmail(SENDER, recipients, msg.as_string())
        print(f"✅ Sent to: {', '.join(recipients)}")
    except Exception as e:
        print(f"[Email Error] {e}")
