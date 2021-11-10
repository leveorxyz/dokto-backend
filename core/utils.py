import os
from django.core.mail import EmailMultiAlternatives
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


def send_mail(subject, to_email, input_context, template_name, cc_list=[], bcc_list=[]):
    """
    Send Activation Email To User
    """
    base_url = input_context.pop("host_url").split("/")
    base_url = base_url[0] + "//" + base_url[2]

    print(base_url)
    context = {
        "site": "dokto",
        "MEDIA_URL": base_url + settings.MEDIA_URL[:-1],
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
