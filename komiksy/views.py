from django.shortcuts import render, redirect
from .forms import ComicForm, ElementsForm
from django.http import Http404
from .models import Comic, User, Elementy
from django.forms import modelformset_factory
from django.views.generic import CreateView,  UpdateView
from PIL import Image, ImageDraw, ImageFont, ImageFile
import uuid


"""
TODO
Przegląd uzytkowników

"""

def home(request):
    last_comics = Comic.objects.filter(publiczny=1)[:1]
    return render(request, 'home.html', {'last_comics':last_comics})


def postacie(request):
    return render(request, 'postacie.html')


def stworz_komiks(request):
    return render(request, 'stworz_komiks.html')


def detail(request, comic_id):
    try:
        comic = Comic.objects.get(pk = comic_id)
    except Comic.DoesNotExist:
        raise Http404("Podany komiks nie istnieje")
    return render(request, 'detail.html', {'comic': comic})


def profil(request, owner_id):
    try:
        user_id = owner_id
        owner = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("Podany użytkownik nie istnieje")
    comics = Comic.objects.filter(owner_id=user_id)
    context = {
        'owner': owner,
        'comics': comics,
    }
    return render(request, 'profil.html', context)


def delete_comic(request, comic_id):
    if request.user.is_authenticated:
        comic = Comic.objects.get(pk=comic_id)
        elementy_id = comic.element.id
        elementy = Elementy.objects.get(pk = elementy_id)
        comic.delete()
        elementy.delete()
    return render(request, 'delete_comic.html')


def delete_elementy(request, elementy_id):
        elementy = Elementy.objects.get(pk=elementy_id)
        elementy.delete()
        return redirect('rysuj')


def rysuj(request):
    form = ElementsForm(request.POST, request.FILES)

    if request.method == 'POST':
        form.instance.background = request.POST.get('background', None)
        form.instance.character1 = request.POST.get('character1', None)
        form.instance.character2 = request.POST.get('character2', None)
        form.instance.chat1 = request.POST.get('chat1', None)
        form.instance.chat2 = request.POST.get('chat2', None)
        form.instance.text1 = request.POST.get('text1', None)
        form.instance.text2 = request.POST.get('text2', None)

        if form.is_valid():
            form.save()

            return redirect('stworzone', elementy_id=form.instance.id)
        else:
            form = ElementsForm()

    return render(request, 'rysuj.html', {
        'form': form})


def stworzone(request, elementy_id):
    elementy = Elementy.objects.get(pk = elementy_id)

    im1 = Image.open(elementy.background)
    img1 = im1.resize((600,600))
    im2 = Image.open(elementy.character1)
    img2 = im2.resize((250,250))
    im3 = Image.open(elementy.character2)
    img3 = im3.resize((250,250))
    im4 = Image.open(elementy.chat1)
    img4 = im4.resize((280,280))
    im5 = Image.open(elementy.chat2)
    img5 = im5.resize((280,280))

    img1.paste(img2, (0, 350), img2)
    img1.paste(img3, (330, 350), img3)
    img1.paste(img4, (30, 50), img4)
    img1.paste(img5, (290, 50), img5)

    t = ''
    t2 = ''

    if len(elementy.text1) <= 70:
        for i, c in enumerate(elementy.text1):
            if i == 20 or i == 40 or i == 60 or i == 70:
                if c == ' ' or c == ',' or c == '.':
                    t += '\n'
                else:
                    t += '-\n'
                t += c
            else:
                t += c
    else:
        t = "Niestety wprowadzony\ntekst jest za dlugi\nsprobuj ponownie"

    if len(elementy.text2) <= 70:
        for i, c in enumerate(elementy.text2):
            if i == 20 or i == 40 or i == 60 or i == 70:
                if c == ' ' or c == ',' or c == '.':
                    t2 += '\n'
                else:
                    t2 += '-\n'
                t2 += c
            else:
                t2 += c
    else:
        t2 = "Niestety wprowadzony\ntekst jest za dlugi\nsprobuj ponownie"




    draw = ImageDraw.Draw(img1)
    font = ImageFont.truetype('/home/ichiraku/Downloads/abhaya-libre/AbhayaLibre-Regular.ttf', 25)
    draw.text((60, 100), t, (0, 0, 0), font=font)
    draw.text((330, 100), t2, (0, 0, 0), font=font)

    filename = str(uuid.uuid4()) + '.png'
    img1.save('media/' + filename)
    img1 = filename
    elementy.background = img1

    form = ComicForm(request.POST, request.FILES)

    if request.method == 'POST':

        form.instance.owner = request.user
        form.instance.comics = elementy.background
        form.instance.element = elementy


        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = ComicForm()

    context = {
        'form': form,
        'elementy': elementy,
    }
    return render(request, 'stworzone.html', context)



def stworz(request, elementy_id):
    elementy = Elementy.objects.get(pk = elementy_id)
    form = ComicForm(request.POST, request.FILES)

    if request.method == 'POST':

        form.instance.owner = request.user
        #form.instance.comics = background elementy

        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = ComicForm()

    context = {
        'form': form,
        'elementy': elementy,
    }
    return render(request, 'stworz.html', context)

def meme_zalogowany(request):
    form = ComicForm(request.POST, request.FILES)
    if request.method =='POST':
        form.instance.owner = request.user
        form.instance.comics = request.FILES["png"]
        if form.is_valid():
            form.save()
            return redirect('meme_zalogowany.html')
        else:
            form = ComicForm()
    return render(request, 'meme_zalogowany.html', {
        'form': form
    })


def rysuj_zalogowany(request):
    return render(request, 'rysuj_zalogowany.html')


def najnowsze(request):
    last_comics = Comic.objects.filter(publiczny=1)[:5]
    return render(request, 'najnowsze.html', {'last_comics':last_comics},)


def kolekcja(request):
    all_comics = Comic.objects.filter(publiczny=1)
    return render(request, 'kolekcja.html',  {'all_comics' : all_comics,})



class ComicEdit(UpdateView):
    template_name = 'edycja.html'
    model = Comic
    fields = [ 'title', 'publiczny']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(MemeCreate, self).form_valid(form)


class MemeCreate(CreateView):
    template_name = 'rysuj_zalogowany.html'
    model = Comic
    fields = [ 'title', 'publiczny']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(MemeCreate, self).form_valid(form)


class ComicCreate(CreateView):
    model = Comic
    fields = ['comics', 'title', 'publiczny']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ComicCreate, self).form_valid(form)

def meme(request):
    ComicFormSet = modelformset_factory(Comic, fields= ('comics', 'type', 'title', 'publiczny'))
    if request.method == 'POST':
        formset = ComicFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return redirect('home.html')
    else:
        formset = ComicFormSet()
    return render(request, 'meme.html', {'formset ': formset})
"""nei dziala

class MemeDelete(DeleteView):
    model = Comic
    template_name = 'delete_comic.html'
    context_object_name = 'comic'
    success_url = reverse_lazy('home') #doc : We have to use reverse_lazy() here, not just reverse as the urls are not loaded when the file is imported.

"""



