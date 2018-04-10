from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm, UserInformationUpdateForm
from komiksy.models import Comic
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


def rejestracja(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'rejestracja.html', {'form': form})


def moje_konto(request):
    comics = Comic.objects.filter(owner=request.user)
    context = {
        'comics': comics,
    }
    return render(request, 'moje_konto.html', context)


def delete_konto(request):
    user = User.objects.get(pk= request.user.id)
    user.delete()
    return redirect('home')


class UserUpdateView(UpdateView):
    form_class = UserInformationUpdateForm
    template_name = 'moje_dane.html'

    def get_object(self):
        return self.request.user


def zmiana_hasla(request):
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Twoje hasło zostało zmienione!')
                return redirect('zmiana_hasla')
            else:
                messages.error(request, 'Proszę spóbować jeszcze raz')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'zmiana_hasla.html', {
        'form': form
    })

