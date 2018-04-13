from django.shortcuts import render, redirect
from .forms import ComicForm, ElementsForm, CommentForm
from django.http import Http404
from .models import Comic, User, Elementy, Favorite, Votes, Subscription, Comments
from django.views.generic import CreateView
from PIL import Image, ImageDraw, ImageFont
from django.db.models import Q
import uuid


def like(request, comic_id):
    comic = Comic.objects.get(pk=comic_id)
    likes = Votes.objects.filter(uzytkownik=request.user, comic= comic)
    if likes.count() > 0:
        return redirect('detail', comic_id)
    l2 = Votes.objects.create(uzytkownik=request.user, comic= comic)
    l2.save()
    comic.likes = comic.likes + 1
    comic.save()
    return redirect('detail', comic_id)


def unlike(request, comic_id):
    comic = Comic.objects.get(pk=comic_id)
    f1 = Votes.objects.get(uzytkownik=request.user, comic=comic)
    f1.delete()
    comic.likes = comic.likes - 1
    comic.save()
    return redirect('detail', comic_id)


def detail(request, comic_id):
    try:
        comic = Comic.objects.get(pk=comic_id)
        subscribed = User.objects.get(pk=comic.owner_id)
        form = CommentForm(request.POST)
        all_comments = Comments.objects.filter(comic = comic)

        if request.user.is_authenticated:
            f = Favorite.objects.filter(uzytkownik=request.user, comic= comic)
            l = Votes.objects.filter(uzytkownik=request.user, comic= comic)
            sub = Subscription.objects.filter(subscribed=subscribed, subscriber=request.user)
            com = Comments.objects.filter(author=request.user, comic = comic)

            if f.count() > 0 and l.count() > 0 and sub.count() > 0 and com.count() > 0:
                fav = Favorite.objects.get(uzytkownik=request.user, comic=comic)
                likes = Votes.objects.get(uzytkownik=request.user, comic=comic)
                subs = Subscription.objects.get(subscribed=comic.owner_id, subscriber=request.user)
                comm = Comments.objects.get(author=request.user, comic=comic)
                context = {
                    'fav': fav,
                    'comic': comic,
                    'likes': likes,
                    'subs': subs,
                    'comm': comm,
                    'all_comments': all_comments,
                }
                return render(request, 'detail.html', context)

            elif f.count() > 0 and l.count() > 0 and sub.count() > 0:
                fav = Favorite.objects.get(uzytkownik=request.user, comic=comic)
                likes = Votes.objects.get(uzytkownik=request.user, comic=comic)
                subs = Subscription.objects.get(subscribed=comic.owner_id, subscriber=request.user)
                context = {
                    'fav': fav,
                    'comic': comic,
                    'likes': likes,
                    'subs': subs,
                    'form': form,
                    'all_comments': all_comments,
                }
                return render(request, 'detail.html', context)

            elif l.count() > 0 and sub.count() > 0 and com.count() > 0:
                likes = Votes.objects.get(uzytkownik=request.user, comic= comic)
                subs = Subscription.objects.get(subscribed=subscribed, subscriber=request.user)
                comm = Comments.objects.get(author=request.user, comic=comic)
                context = {
                    'comic': comic,
                    'likes': likes,
                    'subs': subs,
                    'comm': comm,
                    'all_comments': all_comments,
                }
                return render(request, 'detail.html', context)

            elif f.count() > 0 and l.count() > 0 and com.count() > 0:
                fav = Favorite.objects.get(uzytkownik=request.user, comic=comic)
                likes = Votes.objects.get(uzytkownik=request.user, comic=comic)
                comm = Comments.objects.get(author=request.user, comic=comic)
                context = {
                    'fav': fav,
                    'comic': comic,
                    'likes': likes,
                    'comm': comm,
                    'all_comments': all_comments,
                }
                return render(request, 'detail.html', context)

            elif f.count() > 0 and sub.count() > 0 and com.count() > 0:
                subs = Subscription.objects.get(subscribed=subscribed, subscriber=request.user)
                fav = Favorite.objects.get(uzytkownik=request.user, comic=comic)
                comm = Comments.objects.get(author=request.user, comic =comic)
                context = {
                    'comic': comic,
                    'subs': subs,
                    'fav': fav,
                    'comm': comm,
                    'all_comments': all_comments,
                }
                return render(request, 'detail.html', context)

            elif f.count() > 0 and l.count() > 0:
                fav = Favorite.objects.get(uzytkownik=request.user, comic=comic)
                likes = Votes.objects.get(uzytkownik=request.user, comic=comic)
                context = {
                    'fav': fav,
                    'comic': comic,
                    'likes': likes,
                    'form': form,
                    'all_comments': all_comments,
                }
                return render(request, 'detail.html', context)

            elif l.count() > 0 and sub.count() > 0:
                likes = Votes.objects.get(uzytkownik=request.user, comic= comic)
                subs = Subscription.objects.get(subscribed=subscribed, subscriber=request.user)
                context = {
                    'comic': comic,
                    'likes': likes,
                    'subs': subs,
                    'form': form,
                    'all_comments': all_comments,
                }
                return render(request, 'detail.html', context)

            elif f.count() > 0 and sub.count() > 0:
                subs = Subscription.objects.get(subscribed=subscribed, subscriber=request.user)
                fav = Favorite.objects.get(uzytkownik=request.user, comic=comic)
                context = {
                    'comic': comic,
                    'subs': subs,
                    'fav': fav,
                    'form': form,
                    'all_comments': all_comments,
                }
                return render(request, 'detail.html', context)

            elif sub.count() > 0 and com.count() > 0:
                subs = Subscription.objects.get(subscribed=subscribed, subscriber=request.user)
                comm = Comments.objects.get(author=request.user, comic=comic)
                context = {
                    'comic': comic,
                    'subs': subs,
                    'comm': comm,
                    'all_comments': all_comments,
                }
                return render(request, 'detail.html', context)

            elif f.count() > 0 and com.count() > 0:
                fav = Favorite.objects.get(uzytkownik=request.user, comic=comic)
                comm = Comments.objects.get(author=request.user, comic=comic)
                context = {
                    'comic': comic,
                    'fav': fav,
                    'comm': comm,
                    'all_comments': all_comments,
                }
                return render(request, 'detail.html', context)

            elif l.count() > 0 and com.count() > 0:
                likes = Votes.objects.get(uzytkownik=request.user, comic=comic)
                comm = Comments.objects.get(author=request.user, comic=comic)
                context = {
                    'comic': comic,
                    'likes': likes,
                    'comm': comm,
                    'all_comments': all_comments,
                }
                return render(request, 'detail.html', context)

            elif sub.count() > 0 :
                subs = Subscription.objects.get(subscribed=subscribed, subscriber=request.user)
                context = {
                    'comic': comic,
                    'subs': subs,
                    'form': form,
                    'all_comments': all_comments,
                }
                return render(request, 'detail.html', context)
            elif f.count() > 0 :
                fav = Favorite.objects.get(uzytkownik=request.user, comic=comic)
                context = {
                    'comic': comic,
                    'fav': fav,
                    'form': form,
                    'all_comments': all_comments,
                }
                return render(request, 'detail.html', context)
            elif l.count() > 0:
                likes = Votes.objects.get(uzytkownik=request.user, comic=comic)
                context = {
                    'comic': comic,
                    'likes': likes,
                    'form': form,
                    'all_comments': all_comments,
                }
                return render(request, 'detail.html', context)
            elif com.count() > 0:
                comm = Comments.objects.get(author=request.user, comic=comic)
                context = {
                    'comic': comic,
                    'comm': comm,
                    'all_comments': all_comments,
                }
                return render(request, 'detail.html', context)

        if request.method == 'POST':
            form.instance.text = request.POST.get('text', None)
            form.instance.comic = comic
            form.instance.author = request.user

            if form.is_valid():
                form.save()

                return redirect('detail', comic_id)
            else:
                form = CommentForm()

    except Comic.DoesNotExist:
        raise Http404("Podany komiks nie istnieje")
    return render(request, 'detail.html', {'comic': comic, 'form': form, 'all_comments': all_comments})


def subscribe_comic_owner(request, comic_id):
    comic = Comic.objects.get(pk=comic_id)
    subscribed = User.objects.get(pk = comic.owner_id)
    sub = Subscription.objects.filter(subscribed=subscribed, subscriber=request.user)
    if sub.count() > 0:
        return redirect('detail', comic_id)
    sub1 = Subscription.objects.create(subscribed=subscribed, subscriber=request.user)
    sub1.save()
    return redirect('detail', comic_id)


def unsubscribe_comic_owner(request, comic_id):
    comic = Comic.objects.get(pk=comic_id)
    subscribed = User.objects.get(pk = comic.owner_id)
    sub = Subscription.objects.filter(subscribed=subscribed, subscriber=request.user)
    sub.delete()
    return redirect('detail', comic_id)


def profil(request, owner_id):
    try:
        user_id = owner_id
        owner = User.objects.get(pk=user_id)
        comics = Comic.objects.filter(owner_id=user_id)
        if request.user.is_authenticated:
            sub = Subscription.objects.filter(subscribed=owner, subscriber=request.user)
            if sub.count() > 0 :
                subs = Subscription.objects.get(subscribed=owner, subscriber=request.user)
                context = {
                    'owner': owner,
                    'comics': comics,
                    'subs': subs,
                }
                return render(request, 'profil.html', context)
    except User.DoesNotExist:
        raise Http404("Podany użytkownik nie istnieje")
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


# dodanie elementów komiksów do Elementy
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


# stworzenie komiksów z wybranych Elementów
def stworzone(request, elementy_id):
    try:
        elementy = Elementy.objects.get(pk = elementy_id)

        im1 = Image.open(elementy.background)
        img1 = im1.resize((600, 600))
        im2 = Image.open(elementy.character1)
        img2 = im2.resize((250, 250))
        im3 = Image.open(elementy.character2)
        img3 = im3.resize((250, 250))
        im4 = Image.open(elementy.chat1)
        img4 = im4.resize((280, 280))
        im5 = Image.open(elementy.chat2)
        img5 = im5.resize((280, 280))

        img1.paste(img2, (0, 350), img2)
        img1.paste(img3, (330, 350), img3)
        img1.paste(img4, (30, 50), img4)
        img1.paste(img5, (290, 50), img5)

        t = ''
        t2 = ''

        if len(elementy.text1) <= 70:
            for i, c in enumerate(elementy.text1):
                if i == 18 or i == 36 or i == 54 or i == 70:
                    if c == ' ' or c == ',' or c == '.':
                        t += '\n'
                    else:
                        t += '-\n'
                    t += c
                else:
                    t += c
        else:
            t = "Wprowadzony\ntekst jest za dlugi.\nProszę spróbować\nponownie"

        if len(elementy.text2) <= 70:
            for i, c in enumerate(elementy.text2):
                if i == 18 or i == 36 or i == 54 or i == 70:
                    if c == ' ' or c == ',' or c == '.':
                        t2 += '\n'
                    else:
                        t2 += '-\n'
                    t2 += c
                else:
                    t2 += c
        else:
            t2 = "Wprowadzony\ntekst jest za dlugi.\nProszę spróbować\nponownie"

        draw = ImageDraw.Draw(img1)
        font = ImageFont.truetype('/home/ichiraku/Downloads/abhaya-libre/AbhayaLibre-Regular.ttf', 25)
        draw.text((60, 100), t, (0, 0, 0), font=font)
        draw.text((320, 100), t2, (0, 0, 0), font=font)

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
    except Elementy.DoesNotExist:
        raise Http404("Podany komiks nie istnieje")
    return render(request, 'stworzone.html', context)


def stworz(request, elementy_id):
    elementy = Elementy.objects.get(pk = elementy_id)
    form = ComicForm(request.POST, request.FILES)

    if request.method == 'POST':

        form.instance.owner = request.user

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


def favorite(request, comic_id):
    comic = Comic.objects.get(pk=comic_id)
    f = Favorite.objects.filter(uzytkownik=request.user, comic=comic)
    if f.count() > 0:
        return redirect('detail', comic_id)
    f2 = Favorite.objects.create(uzytkownik=request.user, comic=comic)
    f2.save()
    return redirect('detail', comic_id)


def unfavorite(request, comic_id):
    comic = Comic.objects.get(pk=comic_id)
    f1 = Favorite.objects.get(uzytkownik=request.user, comic= comic)
    f1.delete()
    return redirect('detail', comic_id)


def subscribe_user(request, owner_id):
    subscribed = User.objects.get(pk=owner_id)
    sub = Subscription.objects.filter(subscribed=subscribed, subscriber=request.user)
    if sub.count() > 0:
        return redirect('profil', owner_id)
    sub1 = Subscription.objects.create(subscribed=subscribed, subscriber=request.user)
    sub1.save()
    return redirect('profil', owner_id)


def unsubscribe_user(request, owner_id):
    subscribed = User.objects.get(pk=owner_id)
    sub = Subscription.objects.filter(subscribed=subscribed, subscriber=request.user)
    sub.delete()
    return redirect('profil', owner_id)


def uzytkownicy(request):
    users = User.objects.filter(is_superuser=0)
    comics = Comic.objects.all()
    query = request.GET.get("q")
    if query:
        users = users.filter(
            Q(username__contains=query)
        )
    context = {
        'users': users,
        'comics': comics,
    }
    return render(request, 'uzytkownicy.html', context)


def kolekcja(request):
    all_comics = Comic.objects.filter(publiczny=1)
    comm = Comments.objects.filter(comic=all_comics)
    query = request.GET.get("q")
    if query:
        all_comics = all_comics.filter(
            Q(title__contains=query)
        )
    context = {
        'all_comics': all_comics,
        'comm': comm,
    }
    return render(request, 'kolekcja.html',  context)


def home(request):
    last_comics = Comic.objects.filter(publiczny=1)[:1]
    return render(request, 'home.html', {'last_comics': last_comics})


def postacie(request):
    return render(request, 'postacie.html')


# 10 najlepszych komiksów, sortowne od największej ilości lajkow
def najlepsze(request):
    comics = Comic.objects.filter(publiczny=1, likes__gt=0).order_by('-likes')[:10]
    return render(request, 'najlepsze.html', {'comics': comics})


def moje_sub(request):
    users = Subscription.objects.filter(subscriber=request.user)
    return render(request, 'moje_sub.html', {'users': users})


def polubione(request):
    comics = Votes.objects.filter(uzytkownik=request.user)
    return render(request, 'polubione.html', {'comics': comics})


def ulubione(request):
    comics = Favorite.objects.filter(uzytkownik=request.user)
    return render(request, 'ulubione.html', {'comics': comics})


def moje_komentarze(request):
    comm = Comments.objects.filter(author=request.user)
    return render(request, 'moje_komentarze.html', {'comm': comm})


def usun_komentarz(request, comm_id):
    comm = Comments.objects.get(pk = comm_id)
    comm.delete()
    return render(request, 'usun_komentarz.html')


def usun_komentarz2(request, comm_id):
    comm = Comments.objects.get(pk = comm_id)
    comm.delete()
    return render(request, 'usun_komentarz.html')



class ComicCreate(CreateView):
    model = Comic
    fields = ['comics', 'title', 'publiczny']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ComicCreate, self).form_valid(form)





