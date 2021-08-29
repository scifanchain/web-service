from django.shortcuts import render, redirect, get_object_or_404
import python_avatars as pa
from django.conf import settings
from django.http import HttpResponse

from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

from works.models import Stage
from .forms import StageForm


def change_avatar(request):
    if request.user.is_authenticated:
        path = settings.BASE_DIR / "media/avatars/{}".format(request.user.date_joined.year)
        random_avatar = pa.Avatar.random()
        random_avatar.render("{}/{}.svg".format(path, request.user.username))

        res = "/media/avatars/" + format(request.user.date_joined.year) + "/" + request.user.username
    else:
        res = ''
    return HttpResponse(res)


def change_password(request):
    return render(request, 'space/change_password.html')


def home(request):
    return render(request, 'space/home.html')


def profile(request):
    return render(request, 'space/profile.html')


def works(request):
    stages = Stage.objects.all()
    return render(request, 'space/works.html', {"stages": stages})


def stage(request, stage_id):
    stage = get_object_or_404(Stage, pk=stage_id)
    return render(request, 'space/stage.html', {'stage': stage})


def create_work(request):
    return render(request, 'space/create_work.html')


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

    return render(request, 'space/wallet.html')
