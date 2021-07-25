from django import forms
from django.forms import ModelForm
from blog.models import post,Profile,comment
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User,auth

class PostCreateForm(ModelForm):
    class Meta:
        model = post
        fields = ['title','body','status','restrict_comment']



class PostEditForm(ModelForm):
    class Meta:
        model = post
        fields = ['title','body','status','restrict_comment']



class UserLoginForm(forms.Form):
    username=forms.CharField(label="")
    password=forms.CharField(label="",widget=forms.PasswordInput)

# -----------------------------------------------------------------------------------

class UserRegistrationForm(ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs = {'placeholder': 'Enter the password'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs = {'placeholder': 'confirm password'}))
    print('class waali jagah')
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

    def clean_confirm_password(self):
        password=self.cleaned_data.get('password')
        confirm_password=self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("password mismatch")
        return confirm_password
            
class UserEditForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = User
        fields = ("username","first_name","last_name","email")



class ProfileEditForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        exclude = ("user",)



class commentForm(forms.ModelForm):
    content=forms.CharField(label="",widget=forms.Textarea(attrs={'class':'form-control','placeholder':'text goes here','rows':'2','cols':'50'}))
    class Meta:
        model = comment
        fields = ("content",)


        
