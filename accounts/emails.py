from django.core.mail import send_mail
from django.conf import settings

def send_raw_email(email, subject, message):
    send_mail(subject, message, f"Genesis gallery <{settings.EMAIL_HOST_USER}>", [email])