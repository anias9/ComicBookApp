from django.forms import ModelForm, forms
from .models import Comic, Elementy, Comments


class ComicForm(ModelForm):

    class Meta:
        model = Comic
        fields = ('title', 'publiczny')


class ElementsForm(ModelForm):
    class Meta:
        model = Elementy
        fields = ('text1', 'text2')


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ('text', )


class ComicUpdateForm(ModelForm):

    class Meta:
        model = Comic
        fields = ('publiczny', 'title')