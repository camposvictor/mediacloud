from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from core.models import CustomUser
from .models import MediaFile



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    name = forms.CharField(max_length=100, help_text='Required. Inform your full name.')
    profile_picture = forms.ImageField(required=False, help_text='Optional. Upload your profile picture.')

    class Meta:
        model = CustomUser
        fields = ('username', 'name', 'email', 'password1', 'password2', 'profile_picture')



class EditProfileForm(UserChangeForm):
    name = forms.CharField(max_length=100, help_text='Required. Inform your full name.')
    profile_picture = forms.ImageField(required=False, help_text='Optional. Upload your profile picture.')

    class Meta:
        model = CustomUser
        fields = ('username', 'name', 'profile_picture')

class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ['file', 'media_type', 'description']

