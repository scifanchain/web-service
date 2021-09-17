from django.shortcuts import render, redirect
from .models import Channel, Topic
from .forms import TopicForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    channels = Channel.objects.all()
    topics = Topic.objects.all()
    total = Topic.objects.count()
    return render(request, 'community/home.html', {'channels':channels, 'topics':topics, 'total':total})

def channel(request, channel_id):
    channels = Channel.objects.all()
    topics = Topic.objects.all().filter(channel=channel_id)
    total = Topic.objects.filter(channel=channel_id).count()

    return render(request, 'community/home.html', {'channels':channels, 'topics':topics, 'total':total, 'channel_id':channel_id})

def topic_list(request, topic_id):
    return render(request, 'community/topic_list.html')

@login_required()
def create_topic(request):
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            return redirect('/community/')
    else:
        form = TopicForm()
    return render (request, 'community/topic.html', {'form':form})

