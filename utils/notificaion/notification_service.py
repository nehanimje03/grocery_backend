# Django Imports
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend

# Third-Party Imports
from rest_framework.response import Response
from rest_framework import status

# Local Project Imports
from utils.api.error_code import *


from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend


def send_emails(
        smtp_config,
        recipient_email,
        subject,
        html_body,
        plain_text_body=None
):
    try:
        if not smtp_config:
            return False, "SMTP configuration not found"

        if smtp_config.is_deactive:
            return False, "SMTP configuration is inactive"

        email_backend = EmailBackend(
            host=smtp_config.smtp_host,
            port=smtp_config.smtp_port,
            username=smtp_config.smtp_host_user,
            password=smtp_config.smtp_host_password,
            use_tls=smtp_config.encryption_type == "TLS",
            use_ssl=smtp_config.encryption_type == "SSL",
            fail_silently=False
        )

        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_text_body or "",
            from_email=smtp_config.from_email,
            to=[recipient_email],
            connection=email_backend
        )

        email.attach_alternative(
            html_body,
            "text/html"
        )

        result = email.send()

        if result == 1:
            return True, None

        return False, "Email was not accepted by SMTP server"

    except Exception as e:
        return False, str(e)
