
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.widgets import ClearableFileInput
from django.shortcuts import render, redirect, get_object_or_404
import python_avatars as pa
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from rest_framework.views import APIView

from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

from works.models import Stage
from .models import Wallet
from .forms import StageForm
from scifanchain.forms import SetPasswordForm

from django.core.paginator import Paginator

from authors.permissions import IsSelfOrReadOnly
from authors.serializers import UserRegisterSerializer, WalletSerializer

from rest_framework.decorators import api_view, permission_classes

import json

from authors.serializers import UserDescSerializer


class UserViewSet(viewsets.ModelViewSet):
    """用户视图集"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()


class WalletViewSet(viewsets.ModelViewSet):
    """钱包视图集"""
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    # lookup_field = 'owner_id'

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MyWallets(APIView):
    """用户钱包"""

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]

        return super().get_permissions()

    def get(self, request, owner_id):
        queryset = Wallet.objects.filter(
            owner_id=owner_id).first()  # 当前只允许用户拥有一个钱包
        # serializer = WalletSerializer(queryset, many=True) # 多个钱包
        serializer = WalletSerializer(queryset)
        return Response(serializer.data)


class ChangeAvatar(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        path = settings.BASE_DIR / \
            "media/avatars/{}".format(request.user.date_joined.year)
        random_avatar = pa.Avatar.random()
        random_avatar.render("{}/{}.svg".format(path, request.user.username))

        res = "media/avatars/" + \
            format(request.user.date_joined.year) + "/" + request.user.username

        return HttpResponse(res)


# 修改密码
def change_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SetPasswordForm(request.user)

    return render(request, 'authors/change_password.html', {'form': form})


# 个人空间首页
@login_required
def home(request):
    return render(request, 'authors/home.html')


# 个人信息
def profile(request):
    return render(request, 'authors/profile.html')


# 作品
def works(request):
    stages = Stage.objects.filter(owner=request.user.id)

    paginator = Paginator(stages, 20)  # 每页1条记录
    page = request.GET.get('page', 1)  # 获取当前page页码，默认为1
    try:
        page_obj = paginator.page(page)  # 分页
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    is_paginated = True if paginator.num_pages > 1 else False
    page_range = paginator.get_elided_page_range(
        page, on_each_side=4, on_ends=3)
    context = {'page_obj': page_obj, 'paginator': paginator,
               'is_paginated': is_paginated, 'page_range': page_range}

    return render(request, 'authors/works.html', context)


def get_stage(request, stage_id):
    stage = get_object_or_404(Stage, pk=stage_id)
    return render(request, 'authors/stage.html', {'stage': stage})


def create_stage(request):
    return render(request, 'authors/create_stage.html')


def edit_stage(request, stage_id):
    stage = get_object_or_404(Stage, pk=stage_id)
    return render(request, 'authors/edit_stage.html', {'stage': stage})


def sign_ex(request):
    substrate = SubstrateInterface(
        url="ws://127.0.0.1:9944",
    )

    # keypair = Keypair.create_from_mnemonic('episode together nose spoon dose oil faculty zoo ankle evoke admit walnut')

    keypair = Keypair(ss58_address="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY")

    # keypair = Keypair.create_from_uri('//Alice')


    call = substrate.compose_call(
        call_module='Balances',
        call_function='transfer',
        call_params={
            'dest': '5DAAnrj7VHTznn2AWBemMuyBwZWs6FNFjdyVXUeYum3PTXFy',
            'value': 2 * 10 ** 3
        }
    )

    extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)

    try:
        receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        print("Extrinsic '{}' sent and included in block '{}'".format(
            receipt.extrinsic_hash, receipt.block_hash))
    except SubstrateRequestException as e:
        print("Failed to send: {}".format(e))


    return render(request, 'authors/home.html')


def wallet(request):
    wallet = Wallet.objects.filter(owner_id=request.user.id)
    return JsonResponse({
        'address': wallet.address,
        'publickey': wallet.publickey
    })

# 生成钱包


@permission_classes((IsAuthenticated, ))
def save_wallet(request):
    if request.method == "POST":
        data = json.loads(request.body)
        wallet = Wallet.objects.filter(owner_id=data['user_id']).exists()
        print(data['publickey'])
        if not wallet:
            wallet = Wallet()
            wallet.address = data['address']
            wallet.publickey = str(data['publickey'])
            wallet.owner_id = data['user_id']
            wallet.save()
            return JsonResponse({
                'msg': 'yes',
                'code': 0
            })
        else:
            return JsonResponse({
                'msg': 'you have the wallet',
                'code': 1
            })
    return JsonResponse({
        'msg': "error",
        'code': 2
    })
