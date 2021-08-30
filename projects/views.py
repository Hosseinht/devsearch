from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project
from .forms import ProjectForm
from .util import search_projects


def projects(request):
    projects, search_query = search_projects(request)
    page = request.GET.get('page')
    results = 6
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages  # it gives the last page
        projects = paginator.page(page)

    context = {'projects': projects, 'search_query': search_query, 'paginator': paginator}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project_obj = Project.objects.get(id=pk)
    return render(request, 'projects/project.html', {'project': project_obj})


@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            # return redirect('project', pk=form.instance.pk)
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'delete_template.html', context)
