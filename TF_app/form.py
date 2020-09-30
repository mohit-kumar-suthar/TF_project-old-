from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import re

class login(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)

    def __init__(self,*args,**kwargs):
        super(login, self).__init__(*args,**kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Username',
        'autocomplete':'off',
        })

        self.fields['password'].widget = forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Password',
        'autocomplete':'off',
        })
    

class register(forms.Form):
    username=forms.CharField(max_length=20)
    email=forms.EmailField()
    password=forms.CharField(max_length=20)
    re_password=forms.CharField(max_length=20)

    def __init__(self,*args,**kwargs):
        super(register, self).__init__(*args,**kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder':'Username',
            'autocomplete':'off',
        })
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder':'Email',
            'autocomplete':'off',
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder':'Password',
            'autocomplete':'off'
        })
        
        self.fields['re_password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder':'Confirm Password',
            'autocomplete':'off',
        })

    def clean_username(self):
        char = re.compile(r'[@!#$%^&*()<>?/\|}{~:]') 
        username = self.cleaned_data['username']
        if ' ' in username:
            raise ValidationError(_('username must without space'))
        if char.search(username) == None:
            pass
        else:
            raise ValidationError(_("Username contain only underscore"))
        if User.objects.filter(username=username).exists():
            raise ValidationError(_("%(username)s Already Exists"),code='invalid',params={'username':username})
        return username

    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("%(email)s Already Exists"),code='invalid',params={'email':email})
        return email

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('re_password')
        if(len(password)<=8 and len(confirm_password)<=8):
            raise ValidationError(_("Password length must 8 "))
        if re.search('[A-Z]', password)!=None and re.search('[0-9]', password)!=None and re.search('[^A-Za-z0-9]', password)!=None:
            pass
        else:
            raise ValidationError(_("password must strong"),code='invalid')
        if(password != confirm_password):
            raise ValidationError(_("Password must match"),code='invalid')
        return confirm_password




            



