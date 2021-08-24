from django.shortcuts import render, redirect
import python_avatars as pa
import datetime
from django.conf import settings

from django.contrib.auth import authenticate

def change_avatar(request):
    if request.user.is_authenticated:
        path = settings.BASE_DIR / "media/avatars/{}".format(request.user.date_joined.year)
        random_avatar = pa.Avatar.random()
        random_avatar.render("{}/{}.svg".format(path, request.user.username))
        return redirect('space:home')
    else:
        return False


def home(request):
    return render(request, 'space/home.html')
