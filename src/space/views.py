from django.shortcuts import render, redirect, get_object_or_404
import python_avatars as pa
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

from works.models import Stage
from .models import Wallet
from .forms import StageForm
from scifanchain.forms import SetPasswordForm

from django.core.paginator import Paginator

import json

# 修改头像
def change_avatar(request):
    if request.user.is_authenticated:
        path = settings.BASE_DIR / \
            "media/avatars/{}".format(request.user.date_joined.year)
        random_avatar = pa.Avatar.random()
        random_avatar.render("{}/{}.svg".format(path, request.user.username))

        res = "/media/avatars/" + \
            format(request.user.date_joined.year) + "/" + request.user.username
    else:
        res = ''
    return HttpResponse(res)


# 修改密码
def change_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SetPasswordForm(request.user)

    return render(request, 'space/change_password.html', {'form': form})


# 个人空间首页
@login_required
def home(request):
    return render(request, 'space/home.html')


# 个人信息
def profile(request):
    return render(request, 'space/profile.html')


# 作品
def works(request):
    stages = Stage.objects.filter(owner=request.user.id)

    paginator = Paginator(stages, 20) # 每页1条记录
    page = request.GET.get('page', 1) # 获取当前page页码，默认为1
    try:
        page_obj = paginator.page(page) # 分页
    except PageNotAnInteger:
        page_obj = paginator.page(1) 
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    is_paginated = True if paginator.num_pages > 1 else False
    page_range = paginator.get_elided_page_range(page, on_each_side=4, on_ends=3)
    context = {'page_obj': page_obj, 'paginator': paginator,
               'is_paginated': is_paginated, 'page_range': page_range}

    return render(request, 'space/works.html',context)


def get_stage(request, stage_id):
    stage = get_object_or_404(Stage, pk=stage_id)
    return render(request, 'space/stage.html', {'stage': stage})


def create_stage(request):
    return render(request, 'space/create_stage.html')


def edit_stage(request, stage_id):
    stage = get_object_or_404(Stage, pk=stage_id)
    return render(request, 'space/edit_stage.html', {'stage': stage})


def sign_ex(request):
    substrate = SubstrateInterface(
        url="ws://127.0.0.1:9944",
    )

    keypair = Keypair.create_from_mnemonic(
        'episode together nose spoon dose oil faculty zoo ankle evoke admit walnut')

    call = substrate.compose_call(
        call_module='Balances',
        call_function='transfer',
        call_params={
            'dest': '5E9oDs9PjpsBbxXxRE9uMaZZhnBAV38n2ouLB28oecBDdeQo',
            'value': 1 * 10**12
        }
    )

    extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)

    try:
        receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        print("Extrinsic '{}' sent and included in block '{}'".format(
            receipt.extrinsic_hash, receipt.block_hash))

    except SubstrateRequestException as e:
        print("Failed to send: {}".format(e))

    return render(request, 'space/sign_ex.html', {'receipt': receipt})

@login_required
def wallet(request):
    wallet = Wallet.objects.filter(owner_id=request.user.id)
    return render(request, 'space/wallet.html', {
        'wallet': wallet
    })

# 生成钱包
@require_POST
@csrf_protect
def create_wallet(request):
    if request.method == "POST":
        data = json.loads(request.body)
        wallet = Wallet.objects.get(owner_id=request.user.id)
        if not wallet:
            wallet = Wallet()
            wallet.address = data['address']
            wallet.publickey = data['publickey']
            wallet.owner = request.user
            wallet.save()
            return JsonResponse({
                'msg':'yes',
                'code':0
                })
        else:
            return JsonResponse({
                'msg':'you have the wallet',
                'code':1
                })
    return JsonResponse({
        'msg':"error",
        'code':2
    })

