"""Email alerting for the anomaly monitor.

A thin, importable notifier: build a plain-text alert from flagged rows and send
it over SMTP. Credentials and server settings come from environment variables
(see ``.env.example``), never from source. Importing this module has no side
effects; nothing is sent unless ``send_alert()`` is called with real settings.

Typical use, chained onto the monitor:

    from anomaly_monitor import load_metrics, compute_rolling_stats, detect_deviations
    from email_alerts import format_alert, send_alert, SmtpSettings

    flagged = detect_deviations(compute_rolling_stats(load_metrics(path)))
    if not flagged.empty:
        send_alert(format_alert(flagged), SmtpSettings.from_env())
"""

from __future__ import annotations

import os
import smtplib
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd


@dataclass(frozen=True)
class SmtpSettings:
    """SMTP connection settings, sourced from the environment."""

    host: str
    port: int
    username: str
    password: str
    sender: str
    recipient: str

    @classmethod
    def from_env(cls) -> SmtpSettings:
        """Build settings from ``ALERT_SMTP_*`` environment variables.

        Fails loudly with a clear message if a required variable is unset, so a
        misconfiguration surfaces immediately instead of sending nowhere or to
        the wrong address.
        """
        try:
            return cls(
                host=os.environ["ALERT_SMTP_HOST"],
                port=int(os.environ.get("ALERT_SMTP_PORT", "587")),
                username=os.environ["ALERT_SMTP_USER"],
                password=os.environ["ALERT_SMTP_PASSWORD"],
                sender=os.environ["ALERT_SENDER"],
                recipient=os.environ["ALERT_RECIPIENT"],
            )
        except KeyError as missing:
            raise KeyError(
                f"missing required environment variable: {missing}"
            ) from None


def format_alert(flagged: pd.DataFrame) -> str:
    """Render flagged rows into a readable plain-text alert body."""
    lines = [
        "Significant deviations were detected in today's metrics:",
        "",
        flagged.to_string(index=False),
        "",
        "This is an automated message from the metric monitor.",
    ]
    return "\n".join(lines)


def send_alert(
    body: str,
    settings: SmtpSettings,
    subject: str = "ALERT: metric deviation detected",
) -> None:
    """Send the alert body over SMTP using the supplied settings (STARTTLS)."""
    message = MIMEMultipart()
    message["From"] = settings.sender
    message["To"] = settings.recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(settings.host, settings.port) as server:
        server.starttls()
        server.login(settings.username, settings.password)
        server.sendmail(settings.sender, settings.recipient, message.as_string())
