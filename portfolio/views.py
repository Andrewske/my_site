from django.core.mail import EmailMessage, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .forms import ContactForm
from .models import Technologies
from django.views.generic import ListView
from my_site import giphy

class HomeListView(ListView):
    model = Technologies
    template_name = 'portfolio/homepage.html'
    context_object_name = 'technologies'
    ordering = ['-date_added']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(HomeListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['welcome_gif'] = giphy.get_gif("welcome")
        return context
    

def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                EmailMessage(subject, 
                            message, 
                            'admin@kevinandrews.info', 
                            ['admin@kevinandrews.info'], 
                            reply_to=[from_email]
                )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "portfolio/contact.html", {'form':form})

def successView(request):
    return HttpResponse('Thank you for your message. I will reply as soon as I am able.')


