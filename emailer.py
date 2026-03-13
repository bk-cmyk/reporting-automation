from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage


class EmailSender:
    def __init__(self) -> None:
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
        self.email_from = os.getenv("EMAIL_FROM")

    def send_bullets(self, recipients: list[str], subject: str, bullets: list[str]) -> None:
        self._validate_config()

        message = EmailMessage()
        message["From"] = self.email_from
        message["To"] = ", ".join(recipients)
        message["Subject"] = subject
        message.set_content(self._build_body(bullets))

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as smtp:
            if self.smtp_use_tls:
                smtp.starttls()
            smtp.login(self.smtp_username, self.smtp_password)
            smtp.send_message(message)

    @staticmethod
    def _build_body(bullets: list[str]) -> str:
        body_lines = ["Here is your KPI summary:", ""]
        body_lines.extend([f"- {line}" for line in bullets])
        return "\n".join(body_lines)

    def _validate_config(self) -> None:
        missing = [
            name
            for name, value in {
                "SMTP_HOST": self.smtp_host,
                "SMTP_PORT": self.smtp_port,
                "SMTP_USERNAME": self.smtp_username,
                "SMTP_PASSWORD": self.smtp_password,
                "EMAIL_FROM": self.email_from,
            }.items()
            if value in (None, "")
        ]

        if missing:
            raise RuntimeError(
                f"Missing email configuration environment variables: {', '.join(missing)}"
            )
