from django.shortcuts import render
from website.forms import NewsLetterForm, ContactForm
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.

def index_view(request):
    return render(request, 'website/index.html')

def about_view(request):
    return render(request, 'website/about.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'Your ticket submited successfully')
            form.save()
        else:
            messages.add_message(request, messages.ERROR, 'Your ticket did not  submited')

    form = ContactForm()
    return render(request, 'website/contact.html', {'form': form})

def newsletter_view(request):
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'Your ticket submited successfully')
            form.save()
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Your ticket did not  submited')
    else:
        return HttpResponseRedirect('/')