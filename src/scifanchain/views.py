from django.utils.timezone import now
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


# 生成随机语录
def generate_quotation():
    word = Word.objects.order_by('?')[:1]
    return {'word': word}


# 获取JWT的Token令牌
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }

# 生成随机头像


def generate_avatar(username):
    path = settings.BASE_DIR / \
        "media/avatars/{}".format(datetime.datetime.now().year)
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
    random_avatar = pa.Avatar.random()
    random_avatar.render(
        "{}/{}.svg".format(path, username))


# 用户注册
# todo:前端已有验证，但这里仍有待进一步添加更为严格的验证
def register(request):
    resData = {}
    proteced_name = ['community', 'blogs',
                     'blog', 'signup', 'signin', 'sign-in', 'sign-up', 'finance', 'galaxy', 'space', 'eras', 'star', 'stars', 'expedition', 'stage', 'stages', 'story', 'stories', 'spacehub', 'hubs', 'person', 'place', 'event', 'concept', 'contract', 'universe', 'ipfs', 'token', 'tokens', 'nfts', 'scifan', 'sci-fan', 'chain', 'about', 'docs', 'word', 'words', 'work', 'works', 'white-paper', 'white_paper', 'text', 'test', 'home', 'index', 'route', 'list', 'category', 'categories', 'logout', 'login']
    if request.method == 'POST':
        clientData = json.loads(request.body)
        if User.objects.filter(username=clientData['username']).exists():
            resData = {
                'error': True,
                'msg': '已存在同名用户。'
            }
        elif clientData['username'] in proteced_name:
            resData = {
                'error': True,
                'msg': '该用户名与系统路径名称冲突，换一个吧。'
            }
        elif User.objects.filter(email=clientData['email']).exists():
            resData = {
                'error': True,
                'msg': '该邮箱已被注册。'
            }
        else:
            user = User()
            user.username = clientData['username']
            user.email = clientData['email']
            user.set_password(clientData['password'])
            user.is_staff = 1
            user.last_login = datetime.datetime.now()
            user.save()
            tokens = get_tokens_for_user(user)
            resData = {
                'error': False,
                'username': clientData['username'],
                'tokens': tokens
            }
            # avatar
            generate_avatar(clientData['username'])
    else:
        resData = {
            'error': True,
            'msg': '提交数据有误，系统只接受POST方式注册。'
        }

    return JsonResponse(resData, json_dumps_params={'ensure_ascii': False})
