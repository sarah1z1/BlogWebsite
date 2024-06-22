from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import Comment, Post, Profile


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
       
        
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        
        
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']
        

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']