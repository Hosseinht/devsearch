from django.shortcuts import render
from .models import Profile


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
