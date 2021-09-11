from django.shortcuts import render, redirect
from .forms import UserCreationForm
import python_avatars as pa
import os
import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login


def home(request):
    return render(request, 'home.html')


def coming(request):
    return render(request, 'coming.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            # avatar
            path = settings.BASE_DIR / \
                "media/avatars/{}".format(datetime.datetime.now().year)
            is_exists = os.path.exists(path)
            if not is_exists:
                os.makedirs(path)
            random_avatar = pa.Avatar.random()
            random_avatar.render(
                "{}/{}.svg".format(path, form.cleaned_data['username']))

            # login
            messages.success(request, '您已成功注册，欢迎来到赛凡链！')
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)

            return redirect('/space/')
        else:
            print(form.errors)
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
