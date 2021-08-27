from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile


def login_user(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # when a user submit we want to output certain errors if something goes wrong
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        # it take user and password and it will make sure password matches with username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request,'Username or password is incorrect')

    return render(request, 'users/login_register.html')


def logout_user(request):
    logout(request)
    messages.error(request, 'User was logged out')
    return redirect('login')


def profile(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    userprofile = Profile.objects.get(id=pk)

    top_skills = userprofile.skill_set.exclude(description__exact='')
    other_skills = userprofile.skill_set.filter(description='')

    context = {'userprofile': userprofile, 'top_skills': top_skills, 'other_skills': other_skills}
    return render(request, 'users/user_profile.html', context)

# def user_account(request):
#     context = {}
#     return render(request, 'users/account.html', context)
