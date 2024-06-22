from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.models import Q

from .forms import RegisterForm, CommentForm, PostForm, ProfileForm, UserForm
from .models import Post
from django.contrib.auth.models import User


def home(request):
    page = 'home'
    query = ''
    
    if request.GET.get('query'):
        query = request.GET.get('query')
        
    posts = Post.objects.filter(
        Q(title__icontains=query) | 
        Q(author__username__icontains=query) | 
        Q(content__icontains=query)
    ).order_by('-created')
    
    context = {'posts':posts, 'query':query, 'page':page}
    return render(request, 'base/home.html', context)


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "User doesn't exist.")
    
    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registeration.')
            
    context = {'form':form}
    return render(request, 'base/login_register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/login/')
def viewPost(request, pk):
    post = Post.objects.get(pk=pk)
    comments = post.comment_set.all()
    form = CommentForm()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.commenter = request.user
            comment.post = post
            comment.save()
            return redirect('view-post', pk=post.pk)
        
    context = {'post':post, 'form':form, 'comments':comments}
    return render(request, 'base/view_post.html', context)


@login_required(login_url="/login/")
def createPost(request):
    page = 'create'
    form = PostForm()
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
        else:
            messages.error('Something went wrong! try again.')
            
    context = {'form':form, 'page':page}
    return render(request, 'base/post_form.html', context)


@login_required(login_url="/login/")
def updatePost(request, pk):
    user = request.user
    post = user.post_set.get(id=pk)
    form = PostForm(instance=post)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('view-post', pk=post.pk)
    
    context = {'post':post, 'form':form}
    return render(request, 'base/post_form.html', context)


@login_required(login_url="/login/")
def deletePost(request, pk):
    user = request.user
    post = user.post_set.get(id=pk)
    
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    
    context = {'obj': post}
    return render(request, 'base/delete.html', context)


@login_required(login_url="/login/")
def deleteComment(request, pk, commentId):
    post = Post.objects.get(id=pk)
    comment = post.comment_set.get(id=commentId)
    
    if request.method == 'POST':
        comment.delete()
        return redirect('view-post', pk=post.pk)
    
    context = {'obj':comment}
    return render(request, 'base/delete.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all().order_by('-created')
    
    context = {'user':user, 'posts':posts}
    return render(request, 'base/user_profile.html', context)


@login_required(login_url='/login/')
def profile(request):
    user = request.user
    posts = user.post_set.all().order_by('-created')
    comments = user.commenter.all().order_by('-created')
    
    context = {'posts':posts, 'comments':comments}
    return render(request, 'base/my_profile.html', context)


@login_required(login_url='/login/')
def updateProfile(request):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
        
    context = {'user_form':user_form, 'profile_form':profile_form}
    return render(request, 'base/profile_form.html', context)


@login_required(login_url='/login/')
def deleteProfile(request):
    page = 'delete_account'
    profile = request.user.profile
    
    if request.method == 'POST':
        profile.delete()
        return redirect('home')
    
    context = {'obj': profile, 'page': page}
    return render(request, 'base/delete.html', context)


@login_required(login_url='/login/')
def changePassword(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/change_password.html', context)


@login_required(login_url='/login/')
def deleteAccount(request):
    context = {}
    return render(request, 'base/delete_account.html', context)