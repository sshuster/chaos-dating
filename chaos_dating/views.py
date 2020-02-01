# coding=utf-8
from gettext import gettext as _

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from chaos_dating.forms import ProfileForm
from chaos_dating.forms import UserForm


def index(request) -> HttpResponse:
    context = {
        'site': {
            'title': 'Chaos Dating'
        }
    }
    if request.user.is_authenticated:
        return render(request, template_name='chaos_dating/home.html', context=context)
    else:
        return render(request, template_name='chaos_dating/landing.html', context=context)
    

@transaction.atomic
def register(request) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('chaos_dating:index')
    
    user_form = UserCreationForm(data=request.POST or None)
    profile_form = ProfileForm(data=request.POST or None, files=request.FILES or None)
    context = {
        'site': {
            'title': 'Chaos Dating'
        },
        'user_form': user_form,
        'profile_form': profile_form
    }
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
        profile.save()
        login(request, user=user)
        messages.success(request, _('User was successfully registered'))
        return redirect('chaos_dating:index')
    
    return render(request, template_name='registration/register.html', context=context)


def user_login(request) -> HttpResponse:
    login_view = LoginView()
    login_view.setup(request)
    login_view.redirect_authenticated_user = True
    login_view.extra_context = {
        'active': 'login',
        'title': _('Login'),
        'site': {
            'title': 'Chaos Dating'
        },
    }
    return login_view.dispatch(request)


@login_required()
@transaction.atomic
def edit_profile(request) -> HttpResponse:
    user_form = UserForm(data=request.POST or None, instance=request.user)
    profile_form = ProfileForm(data=request.POST or None, files=request.FILES or None,
                               instance=request.user.profile)
    context = {
        'active': 'edit-profile',
        'site': {
            'title': 'Chaos Dating'
        },
        'user_form':    user_form,
        'profile_form': profile_form
    }
    
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile = profile_form.save(commit=False)
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
        profile.save()
        messages.success(request, _('Profile was successfully updated'))

    return render(request, template_name='chaos_dating/edit_profile.html', context=context)


def legal(request) -> HttpResponse:
    context = {
        'site': {
            'title': 'Chaos Dating'
        }
    }
    return render(request, template_name='chaos_dating/legal.html', context=context)


def privacy(request) -> HttpResponse:
    context = {
        'site': {
            'title': 'Chaos Dating'
        }
    }
    return render(request, template_name='chaos_dating/privacy.html', context=context)
