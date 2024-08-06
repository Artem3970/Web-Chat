from django import forms
from django.contrib.auth.models import User
from .models import ChatRoom
from django.contrib.auth.forms import UserCreationForm

class CreateChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name']

class JoinChatRoomForm(forms.Form):
    room_name = forms.CharField(max_length=255, label='Chat Room Name')

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data
