from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .utils import search_profiles
from .models import Profile, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm


def login_user(request):
    page = 'register'
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        username = request.POST['username'].lower()
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
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
            # We can use GET cuz we cleaned the action in login form even thou this is  POST
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
            return redirect('edit-account')
        else:
            messages.error(request, "An error has occurred during registration")

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profile(request):
    # search_query = ''
    #
    # if request.GET.get('search_query'):
    #     search_query = request.GET.get('search_query')
    #
    # skills = Skill.objects.filter(name__icontains=search_query)
    #
    # # distinct = no duplicate
    # profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) |
    #                                              Q(short_intro=search_query) |
    #                                              Q(skill__in=skills)  # query child
    #                                              )
    profiles, search_query = search_profiles(request)

    page = request.GET.get('page')
    results = 6
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages  # it gives the last page
        profiles = paginator.page(page)

    context = {'profiles': profiles, 'search_query': search_query, 'paginator': paginator}
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    userprofile = Profile.objects.get(id=pk)

    top_skills = userprofile.skill_set.exclude(description__exact='')
    other_skills = userprofile.skill_set.filter(description='')

    context = {'userprofile': userprofile, 'top_skills': top_skills, 'other_skills': other_skills}
    return render(request, 'users/user_profile.html', context)


@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile  # request.user= logged in user

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)  # request.Files? for processing picture
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was added successfully")
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated successfully")
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Skill was deleted successfully")
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    message_request = profile.messages.all()  # message = related_name='messages' in Message model
    unread_count = message_request.filter(is_read=False).count()

    context = {'message_request': message_request, 'unread_count': unread_count}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)
