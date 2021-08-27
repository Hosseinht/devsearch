from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import CustomUserCreationForm


def login_user(request):
    page = 'register'
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
            login(request, user)  # create a session base token and add it to cookies
            return redirect('profile')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'users/login_register.html')


def logout_user(request):
    logout(request)
    messages.info(request, 'User was logged out')
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # commit = False? we are saving but we are holding a
            # temporary instance of it. it creates a user object before we processing it.
            # maybe we want to modify something
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User account was created")

            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "An error has occurred during registration")

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


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
