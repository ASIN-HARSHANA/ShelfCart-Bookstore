from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password", "class": "form-control"})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Full Name", "class": "form-control"})
    )
    bio = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Bio", "class": "form-control"})
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Phone", "class": "form-control"})
    )

    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'bio', 'phone']


class OTPVerifyForm(forms.Form):
    otp = forms.CharField(
        max_length=4,           
        min_length=4,           
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center otp-input',
            'placeholder': 'Enter 4-digit OTP',
            'autocomplete': 'off',
            'maxlength': '4',   
            'pattern': '[0-9]{4}',  
            'required': 'required'
        })
    )