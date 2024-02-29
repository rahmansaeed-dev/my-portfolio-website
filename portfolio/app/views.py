from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomModel
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

# Register page 
def Register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phonenumber')
        if len(password) > 10:
            messages.error(request, 'password must be less then 10 character.')
            return redirect('register')
        if len(password) < 8:
            messages.error(request, 'password must be greater than 8 character.')
            return redirect('register')
        if CustomModel.objects.filter(email=email):
            messages.error(request, 'This email is already exit please try other email.')
            return redirect('register')
        reg = CustomModel(first_name=first_name,last_name=last_name, email=email,phonenumber=phone_number)
        reg.set_password(password)
        reg.save()
        messages.success(request, 'You have signed up successfully.')
        return redirect('signin')
    else:
        return render(request, 'register.html')

# Sign in page 
def Sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # import pdb;
        # pdb.set_trace()
        if len(password) > 10:
            messages.error(request, 'password must be less then 10 character.')
            return redirect('signin')
        if len(password) < 8:
            messages.error(request, 'password must be greater than 8 character.')
            return redirect('signin')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'login successully.')
            return redirect('home')
        return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')

# Password Reset view
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.html'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('signin')

# Home page view
def home(request):
    return render(request, 'index.html')

# Base view 
def base(request):
    return render(request, 'base.html')

# Base 1 page view 
def base1(request):
    return render(request, 'base1.html')

# About page view 
def about(request):
    return render(request, 'about-us.html')

# Service page view
def services(request):
    return render(request, 'services.html')

# Contact page view
@login_required(login_url='signin')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if Contact.objects.filter(email=email).exists():
            messages.error(request, 'This email is already in use. Please try another email.')
        else:
            contact = Contact(name=name, email=email, subject=subject, message=message)
            contact.save()
            messages.success(request, 'Thanks for contacting...')
            return redirect('contact')
    return render(request, 'contact.html')

# user logout view
def user_logout(request):
    logout(request)
    return redirect('home')

# portfolio page view 
def portfolio(request):
    return render(request, 'portfolio.html')

