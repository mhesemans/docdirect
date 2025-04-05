from django import forms
from .models import News
from django_summernote.widgets import SummernoteWidget


class NewsPostForm(forms.ModelForm):
    """
    Form for administrative staff to create news posts via frontend.
    Uses Summernote for rich text content editing.
    """

    class Meta:
        model = News
        fields = ['title', 'content', 'status']
        widgets = {
            'content': SummernoteWidget(),
        }
