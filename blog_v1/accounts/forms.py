from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class SignUpForm(UserCreationForm):
    """Форма регистации пользователя"""

    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UpdateUserForm(forms.ModelForm):
    """Форма обновления пользователя"""

    username = forms.CharField(
        max_length=100, required=True, widget=forms.TextInput()
    )
    email = forms.EmailField(required=True, widget=forms.TextInput())

    class Meta:
        model = User
        fields = ["username", "email"]


class UpdateProfileForm(forms.ModelForm):
    """Форма обновления профиля пользователя"""

    avatar = forms.ImageField(widget=forms.FileInput())
    bio = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}))

    class Meta:
        model = Profile
        fields = ["avatar", "bio"]


class ChangePasswordForm(PasswordChangeForm):

    class Meta:
        model = User
