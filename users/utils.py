from django.db.models import Q

from users.models import Skill, Profile


def search_profiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)

    # distinct = no duplicate
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) |
                                                 Q(short_intro=search_query) |
                                                 Q(skill__in=skills)  # query child
                                                 )
    return profiles, search_query
