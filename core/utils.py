from django.core.mail import EmailMultiAlternatives, send_mail as snd_ml
from django.template.loader import render_to_string
from django.conf import settings

from user.models import UserIp


def set_user_ip(request):
    ip = None
    user = request.user
    if request.META.get("HTTP_X_FORWARDED_FOR"):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        ip = request.META.get("REMOTE_ADDR")
    if user.is_authenticated:
        UserIp.objects.update_or_create(user=user, ip_address=ip)


def send_mail(subject=None, message=None, from_email=None, to_email=None, cc_list=[], bcc_list=[]):
    """
    Send Activation Email To User
    """
    # activate_link_url = settings.EMAIL_ACTIVATION_LINK
    # confirmation_token = default_token_generator.make_token(self)

    context = {
        "site": "dokto",
        "link": "https://example.com",
        "provider_name": "test",
        "signature": "dummy",
    }
    # render email text
    email_html_message = render_to_string("email/provider_verification.html", context)

    msg = EmailMultiAlternatives(
        subject=f"Welcome to {context['site']}, please verify your email address",
        body=email_html_message,
        from_email=settings.EMAIL_HOST_USER,
        to=["sihantawsik@gmail.com"],
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
