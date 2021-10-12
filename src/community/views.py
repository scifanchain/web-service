from django.shortcuts import render, redirect, get_object_or_404
from .models import Channel, Topic, Reply
from .forms import TopicForm, ReplyForm
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from scifanchain.permissions import IsAdminUserOrReadOnly

from .serializers import TopicListSerializer


# ViewSets define the view behavior.
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicListSerializer
    # permission_classes = [IsAuthenticated,]
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    # def get_queryset(self):
    #     """
    #     Optionally restricts the returned purchases to a given user,
    #     by filtering against a `username` query parameter in the URL.
    #     """
    #     category_id = self.request.query_params.get('category_id', None)
    #     if category_id is not None:
    #         self.queryset = self.queryset.filter(category=category_id)
    #     return self.queryset

    # def retrieve(self, request, pk=None):
    #     user = get_object_or_404(self.queryset, pk=pk)
    #     serializer = BlogDetailSerializer(user)
    #     return Response(serializer.data)


def home(request):
    channels = Channel.objects.all()
    topics = Topic.objects.all()
    total = Topic.objects.count()
    return render(request, 'community/home.html', {'channels': channels, 'topics': topics, 'total': total})


def channel(request, channel_id):
    channels = Channel.objects.all()
    topics = Topic.objects.all().filter(channel=channel_id)
    total = Topic.objects.filter(channel=channel_id).count()

    return render(request, 'community/home.html', {'channels': channels, 'topics': topics, 'total': total, 'channel_id': channel_id})


def topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    replies = Reply.objects.filter(target=topic_id).all()

    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.target = topic
            obj.owner = request.user
            obj.save()
            return redirect('/community/topic/' + str(topic_id))
    else:
        form = ReplyForm()

    return render(request, 'community/topic.html', {"topic": topic, 'form': form, 'replies': replies})


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
    return render(request, 'community/create_topic.html', {'form': form})
