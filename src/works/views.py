from django.shortcuts import render
from .models import Stage


def index(request):
    return render(request, 'works/index.html')


def detail(request):
    stage = Stage.objects.first()
    return render(request, 'works/detail.html', {'stage':stage})
