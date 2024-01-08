from flatpickr import DatePickerInput
from django_countries.widgets import CountrySelectWidget

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .models import Post, UserProfile, User, Comment, Following

class CreatePostForm(forms.ModelForm):
    content = forms.CharField(label="description", widget=forms.Textarea(attrs={
        'placeholder': _('Share with the world...'),
        'autofocus': 'autofocus',
        'rows':'3',
        'class': 'form-control form',
        'id': 'about-input',
    }))

    class Meta:
        model = Post
        fields = ["content"]


class CreateCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': _('Write a comment'),
        'rows': '1',
    }))

    class Meta:
        model = Comment
        fields = ["content"]

class CreateUserProfileForm(forms.ModelForm):

    date_of_birth = forms.DateField(required=False, label=_("Date of birth: "), widget=forms.DateInput(attrs={
            "type": "date",
            "placeholder": _("Select a date"),
            "class": "form-control"
        }),
    )

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if "default-user.png" not in image:
            if image.size > settings.MAX_UPLOAD_SIZE * 1024 * 1024:
                raise ValidationError(_(f"Image file exceeds {settings.MAX_UPLOAD_SIZE} mb size limit"))
        return image
    
    class Meta:
        model = UserProfile
        fields = ["name", "date_of_birth", "about", "country", "image"]
        labels = {
            "name": _("Name:"),
            "about": _("About:"),
            "country": _("Country:"),
            "image": _("Image:")
        }

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": _("Your name"),
                "class": "form-control"
                }),
            "about": forms.Textarea(attrs={
                "placeholder": _("Tell about yourself"),
                "class": "form-control",
                "id": "about-input",
                "rows": "3"
            }),
            "country": CountrySelectWidget(attrs={
                "class": "form-control"
            }),
        }