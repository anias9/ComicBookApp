"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path, path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.conf import settings
from django.conf.urls.static import static

from konta import views as konta_views
from komiksy import views




urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^comments/', include('django_comments.urls')),

    re_path(r'^zmiana_hasla/$', konta_views.zmiana_hasla, name='zmiana_hasla'),
    re_path(r'^moje_dane/$', konta_views.UserUpdateView.as_view(), name='moje_dane'),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^rejestracja/$', konta_views.rejestracja, name='rejestracja'),
    re_path(r'^logowanie/$', auth_views.LoginView.as_view(template_name='logowanie.html'), name='logowanie'),
    re_path(r'^wyloguj/$', auth_views.LogoutView.as_view(), name='wyloguj'),
    re_path(r'^moje_konto/$', konta_views.moje_konto, name= 'moje_konto'),
    re_path(r'^moje_komentarze/$', views.moje_komentarze, name= 'moje_komentarze'),

    re_path(r'^(?P<comic_id>[0-9]+)/$', views.detail, name='detail'),
    re_path(r'^(?P<comic_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    re_path(r'^(?P<comic_id>[0-9]+)/unfavorite/$', views.unfavorite, name='unfavorite'),
    re_path(r'^(?P<comic_id>[0-9]+)/like/$', views.like, name='like'),
    re_path(r'^(?P<comic_id>[0-9]+)/unlike/$', views.unlike, name='unlike'),

    re_path(r'^(?P<comic_id>[0-9]+)/delete_comic/$', views.delete_comic, name='delete_comic'),
    re_path(r'^(?P<elementy_id>[0-9]+)/delete_elementy/$', views.delete_elementy, name='delete_elementy'),
    re_path(r'^stworz/(?P<elementy_id>[0-9]+)/$', views.stworz, name= 'stworz'),

    re_path(r'^profil/(?P<owner_id>[0-9]+)/$', views.profil, name='profil'),
    re_path(r'^stworzone/(?P<elementy_id>[0-9]+)/$', views.stworzone, name= 'stworzone'),

    re_path(r'^comic_form/$', views.ComicCreate.as_view(), name= 'comic_form'),

    re_path(r'^postacie/$', views.postacie, name= 'postacie'),
    re_path(r'^ulubione/$', views.ulubione, name= 'ulubione'),
    re_path(r'^kolekcja/$', views.kolekcja, name= 'kolekcja'),
    re_path(r'^najlepsze/$', views.najlepsze, name= 'najlepsze'),
    re_path(r'^uzytkownicy/$', views.uzytkownicy, name= 'uzytkownicy'),
    re_path(r'^sample/$', views.sample, name= 'sample'),
    re_path(r'^rysuj/$', views.rysuj, name= 'rysuj'),
    re_path(r'^najnowsze/$', views.najnowsze, name= 'najnowsze'),
    re_path(r'^profil/$', views.profil, name= 'profil'),

                  #re_path(r'^(?P<comic_id>[0-9]+)/delete_comic/$', views.MemeDelete.as_view(), name='delete_comic'),

    re_path(r'^admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

