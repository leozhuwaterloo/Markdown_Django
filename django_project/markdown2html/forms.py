from django import forms
from .models import Note, Course
from pagedown.widgets import PagedownWidget


class NoteForm(forms.ModelForm):
    publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Note
        fields = [
            "title",
            "content_file",
            "contributor",
            "publish",
        ]


class NoteContentForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget)

    class Meta:
        model = Note
        fields = [
            "content",
        ]


class CourseForm(forms.ModelForm):
    publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Course
        fields = [
            "title",
            "contributor",
            "publish",
        ]
