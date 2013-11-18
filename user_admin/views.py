from django import forms
from django.forms.formsets import formset_factory
from models import NewUserForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from models import Profile_Form
from django.contrib.auth.models import User
from models import Profile
from models import Settings
from models import Settings_Form

def register(request):
    if request.method == 'POST':
        span = {1:False}
        form = NewUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = auth.authenticate(
                email=request.POST.get('email', ''),
                password=request.POST.get('password1',''))
            if user is not None:
                auth.login(request, user)
                profile = Profile(user=user)
                profile.save()
                settings = Settings(user=user)
                settings.save()
                return HttpResponseRedirect("/create/profile/")
            else:
                span[1] = True
                form = NewUserForm()
    else:
        form = NewUserForm()
        span = {1:False}
    return render(request, "registration/register.html", {
        'form': form,
        'span': span
        })

def login(request):
    errors = False
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/accounts/profile/")
            else:
                errors = True
        else:
            errors = True

    return render(request, "registration/login.html", {
        'errors': errors,
        })

@login_required
def create_profile(request):

    user = request.user
    profile = user.profile

    if request.method == 'POST':
        created = Profile_Form(request.POST, request.FILES, instance=profile)
        if created.is_valid():
            profile.pic = created.cleaned_data['pic']
            profile.save()
            return HttpResponseRedirect("/accounts/profile/")
        else:
            profileForm = Profile_Form(instance=profile)

    else:
        profileForm = Profile_Form(instance=profile)

    return render(request, "registration/create_profile.html", {
        'form': profileForm,
        'user': user
        })

@login_required
def settings(request):
    user = request.user
    settings = user.settings
    if request.method == 'POST':
        span = False
        updated = Settings_Form(request.POST, instance=settings)
        if updated.is_valid():
            settings = updated
            settings.save()
            span = "Your settings have been saved successfully!"
            settings = user.settings
            settingsForm = Settings_Form(instance=settings)
        else:
            span = "Oops, Something went wrong! Your settings were not saved."
            settingsForm = Settings_Form(instance=settings)

    else:
        span = False
        settingsForm = Settings_Form(instance=settings)

    return render(request, "user/settings.html", {
        'form': settingsForm,
        'user': user,
        'span': span,
        })

@login_required
def profile(request):
    user = request.user
    profile = request.user.profile

    return render(request, "user/profile.html", {
        'user': user,
        'profile': profile,
        })
