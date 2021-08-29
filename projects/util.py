from django.db.models import Q

from projects.models import Tag, Project


def search_projects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(Q(title__icontains=search_query) |
                                                 Q(description__icontains=search_query) |
                                                 Q(owner__name__contains=search_query) |  # parent
                                                 Q(tags__in=tags)
                                                 )

    return projects, search_query
