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
    
def services(request):
    return render(request, 'website/services.html')
    
def handler404(request, exception):
    return render(request, 'error_codes/404.html', status=404)

def handler500(request):
    return render(request, 'error_codes/500.html', status=500)

def handler403(request, exception):
    return render(request, 'error_codes/403.html', status=403)