from backend.app.core.config import settings
from backend.app.core.emails.base import EmailTemplate


class TOTPEnabledEmail(EmailTemplate):
    template_name = "totp_alert.html"
    template_name_plain = "totp_alert.txt"
    subject = "Security Alert: New Authenticator App Linked"


async def send_totp_enabled_email(email: str) -> None:
    context = {
        "site_name": settings.SITE_NAME,
        "support_email": settings.SUPPORT_EMAIL,
    }
    # This calls your base EmailTemplate which queues the Celery task!
    await TOTPEnabledEmail.send_email(email_to=email, context=context)
