from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import UserChangeForm


class CreateUserForm(UserChangeForm):
    password=forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter The Password'})
        )
    confirm_password=forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter The Confirm Password'})
        )
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'confirm_password'
                  ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter The Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter The Email'}),
   
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
            'confirm_password': 'Confirm Password',
        }

class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['profile_pic','username', 'about' ]
        widgets = {
            'profile_pic': forms.FileInput(),
            'username' : forms.TextInput(attrs={'placeholder': 'Add display name'}),
            'about' : forms.Textarea(attrs={'rows':3, 'placeholder': 'Add information'})
        }
        
class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['email']

class PasswordChangeForm(forms.Form):

    old_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter The Old Password'}))
    new_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter The New Password'}))
    confirm_new_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm The New Password'}))



        
      