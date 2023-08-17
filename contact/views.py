from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from user.models import CustomUser
from django.http import HttpResponse

from .forms import ContactForm


def contact_form(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            subject = f'Message form {form.cleaned_data["Topic"]}'
            message = form.cleaned_data["Message"]
            contact_email = form.cleaned_data["Contact_Email"]
            sender = request.user.email
            recipients = ["simbarashemutombe1@gmail.com"]
            try:
                send_mail(
                    subject,
                    "Message: {},\n\n Contact: {}".format(message, contact_email),
                    sender,
                    recipients,
                    fail_silently=True,
                )
            except BadHeaderError:
                return HttpResponse("Invalid header found")
            return HttpResponse("Email sent")
    return render(request, "contact/contact.html", {"form": form})
