from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.core.mail import EmailMessage

from .forms import ContactForm


# Create your views here.
def index(request):
    return render(request, 'landing/index.html')


def contact_submit(request):
    """
    Handle POST from the landing-page contact form:
    - Validate date, send email to company inbox and display message.
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request.")
    
    form = ContactForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Please correct the errors and try again.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    name = form.cleaned_data["name"]
    user_email = form.cleaned_data["email"]
    message = form.cleaned_data["message"]

    subject = f"New contact form submission from {name}"
    body = (
        f"Name: {name}\n"
        f"Email: {user_email}\n\n"
        f"Message:\n{message}\n"
    )

    email_msg = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_RECIPIENT_EMAIL],
        reply_to=[user_email],
    )
    email_msg.send()

    messages.success(request, "Thanks! Your message has been sent.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))