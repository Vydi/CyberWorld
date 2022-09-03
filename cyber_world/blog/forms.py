from django import forms
import re
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from .models import Post


# from captcha.fields import CaptchaField

class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        if value:
            img_html = mark_safe(
                f'<br><br><img class = "image-profile" src="{value.url} " />')
            return f'{input_html}{img_html}'
        return input_html


class PostsForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = "__all__" #для того, чтоб взять все поля из модели
        fields = ['title', 'content', 'photo', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15, }),
            'category': forms.Select(attrs={'class': 'form-control'})
        }
        photo = forms.ImageField(widget=ImagePreviewWidget, label='Фото')

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title


class CommentForm(forms.Form):
    body = forms.CharField(max_length=250, widget=forms.Textarea(
        attrs={
            'rows': 4,
            'cols': 8,
            "class": "com-textarea",
            "placeholder": "Оставьте комментарий (250 символов)"
        })
                           )
