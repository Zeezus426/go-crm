from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404   
from .models import Contact
from .forms import ContactForm
from django.template.loader import get_template
# Create your views here.

# Main page
def index(request):
    contacts = Contact.objects.all()
    return render(request, 'index.html', {'contacts': contacts})


def adding_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)  # Don't save to DB yet
            contact.created_at = timezone.now()  # Set current timestamp
            contact.save()  # Now save to DB
            return redirect('')  # Replace with your desired URL name
    else:
        form = ContactForm()
    return render(request, 'adding_contact.html', {'form': form})