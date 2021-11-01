from django.core.mail import EmailMultiAlternatives, send_mail as snd_ml
from django.template.loader import render_to_string
from django.conf import settings

from user.models import UserIp
from core.classes import ExpiringActivationTokenGenerator


def set_user_ip(request):
    ip = None
    user = request.user
    if request.META.get("HTTP_X_FORWARDED_FOR"):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        ip = request.META.get("REMOTE_ADDR")
    if user.is_authenticated:
        UserIp.objects.update_or_create(user=user, ip_address=ip)


def send_mail(subject, to_email, input_context, template_name, cc_list=[], bcc_list=[]):
    """
    Send Activation Email To User
    """
    confirmation_token = ExpiringActivationTokenGenerator().generate_token(
        text=to_email
    )

    link = "/".join(
        [settings.BACKEND_URL, "activate", confirmation_token.decode("utf-8")]
    )

    context = {
        "site": "dokto",
        "link": link,
        "MEDIA_URL": settings.MEDIA_URL,
        **input_context,
    }

    # render email text
    email_html_message = render_to_string(template_name, context)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=email_html_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email],
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
