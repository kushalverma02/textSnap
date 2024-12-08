from django import forms
from .models import tweets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class TweetForm(forms.ModelForm):
    class Meta:
        model = tweets
        fields =['text','photo']


class UserRegistrationForm(UserCreationForm):
    # email = forms.EmailField()
    class meta:
        model  = User
        fields =('username','email','pasword1','password2')
