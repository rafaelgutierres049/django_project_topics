from django.shortcuts import render
from .models import Topic, Entry
from django_projects.forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    """Página principal"""
    return render(request, 'django_projects/index.html')

@login_required
def topics(request):
    """Mostra os assuntos"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'django_projects/topics.html', context)

@login_required
def topic(request, topic_id):
    """Mostra o topico de acordo com o ID"""
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
            raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries':entries}
    return render(request, 'django_projects/topic.html', context)

@login_required
def new_topic(request):
    """Adiciona um novo assunto"""
    if request.method != 'POST':
        # nenhum dado submetido cria um formulario em branco
        form = TopicForm()
    else:
        # dados de POST submetidos, processo os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))
    
    context = {'form': form}
    return render(request, 'django_projects/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Adiciona nova entrada no tópico"""
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', kwargs={'topic_id': topic_id}))
    context = {'topic':topic, 'form': form}
    return render(request, 'django_projects/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edita uma entrada"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)

    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', kwargs={'topic_id': topic.id}))
        

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'django_projects/edit_entry.html', context)