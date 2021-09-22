from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import UserCreationForm
import python_avatars as pa
import os
import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from works.models import Word
from django.contrib.auth.models import User
from django.db.models import Q

import json


def home(request):
    return render(request, 'home.html')


def coming(request):
    return render(request, 'coming.html')
    

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()

#             # avatar
#             path = settings.BASE_DIR / \
#                 "media/avatars/{}".format(datetime.datetime.now().year)
#             is_exists = os.path.exists(path)
#             if not is_exists:
#                 os.makedirs(path)
#             random_avatar = pa.Avatar.random()
#             random_avatar.render(
#                 "{}/{}.svg".format(path, form.cleaned_data['username']))

#             # login
#             messages.success(request, '您已成功注册，欢迎来到赛凡链！')
#             new_user = authenticate(
#                 username=form.cleaned_data['username'],
#                 password=form.cleaned_data['password1'],
#             )
#             login(request, new_user)

#             return redirect('/space/')
#         else:
#             print(form.errors)
#     else:
#         form = UserCreationForm()

#     word = Word.objects.order_by('?')[:1]

#     return render(request, 'registration/register.html', {'form': form, 'word':word})


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def register(request):
    resData = {}
    if request.method == 'POST':
        clientData = json.loads(request.body)
        if User.objects.filter(username=clientData['username']).exists():
            resData = {
                'error': True,
                'msg': '已存在同名用户。'
            }
        elif User.objects.filter(email=clientData['email']).exists():
            resData = {
                'error': True,
                'msg': '邮箱已被注册。'
            }
        else:
            user = User()
            user.username = clientData['username']
            user.email = clientData['email']
            user.set_password(clientData['password'])
            user.save()
            tokens = get_tokens_for_user(user)
            resData = {
                'error': False,
                'username': clientData['username'],
                'tokens': tokens
            }
    else:
        resData = {
            'error': True,
            'msg': '提交数据有误，系统只接受POST方式注册。'
        }
    
    return JsonResponse(resData, json_dumps_params={'ensure_ascii': False})
