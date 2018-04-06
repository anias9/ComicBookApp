from django.forms import ModelForm, forms
from .models import Comic, Elementy


class ComicForm(ModelForm):

    class Meta:
        model = Comic
        fields = ('title', 'publiczny')


class ElementsForm(ModelForm):
    class Meta:
        model = Elementy
        fields = ('text1', 'text2')