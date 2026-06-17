import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import settings


class EmailService:

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str
    ):

        message = MIMEMultipart()
        message["From"] = settings.SMTP_USER
        message["To"] = to_email
        message["Subject"] = subject

        message.attach(
            MIMEText(html_content, "html")
        )

        with smtplib.SMTP(
            settings.SMTP_HOST,
            settings.SMTP_PORT
        ) as server:

            server.starttls()

            server.login(
                settings.SMTP_USER,
                settings.SMTP_PASSWORD
            )

            server.send_message(message)


email_service = EmailService()