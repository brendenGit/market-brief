"""Send the daily brief (text + mp3 attachment) via Gmail SMTP (free with an app password)."""

import os
import smtplib
from email.message import EmailMessage
from datetime import date


def send_email(subject: str, body_text: str, audio_path: str) -> None:
    gmail_address = os.environ.get("GMAIL_ADDRESS")
    gmail_app_password = os.environ.get("GMAIL_APP_PASSWORD")
    recipient = os.environ.get("RECIPIENT_EMAIL", gmail_address)

    if not gmail_address or not gmail_app_password:
        raise RuntimeError("GMAIL_ADDRESS and GMAIL_APP_PASSWORD environment variables must be set.")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = gmail_address
    msg["To"] = recipient
    msg.set_content(body_text)

    with open(audio_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="audio",
            subtype="mpeg",
            filename=f"market_brief_{date.today().isoformat()}.mp3",
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(gmail_address, gmail_app_password)
        smtp.send_message(msg)


if __name__ == "__main__":
    send_email("Test brief", "This is a test email body.", "test.mp3")
    print("Sent.")
