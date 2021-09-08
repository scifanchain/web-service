from django.shortcuts import render, redirect, get_object_or_404
import python_avatars as pa
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

from works.models import Stage
from .forms import StageForm
from scifanchain.forms import SetPasswordForm


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
    stages = Stage.objects.all()
    return render(request, 'space/works.html', {"stages": stages})


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


def wallet(request):
    substrate = SubstrateInterface(
        url="ws://127.0.0.1:9944",
    )
    mnemonic = Keypair.generate_mnemonic()
    keypair = Keypair.create_from_mnemonic(mnemonic)
    signature = keypair.sign("Test123")

    if keypair.verify("Test123", signature):
        print('Verified')
        print(keypair)

    return render(request, 'space/wallet.html', {'mnemonic': mnemonic, 'keypair': keypair})
