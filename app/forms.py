from django import forms
from app.models import Question, Answer, Tag, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(UserCreationForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']



class SettingsForm(UserChangeForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.profile.avatar = self.cleaned_data['avatar']
        user.profile.save()
        return user


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']
    tags = forms.CharField(required=False)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

