import json

from django.shortcuts import HttpResponse
from django.http import response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
#
from . import models


# Create your views here.


def account_login(request):
    if request.user:
        logout(request)

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    if not user:
        return HttpResponse('wrong')

    login(request, user)
    profile_model = models.ProfileModel.objects.get(id=user.id)

    return HttpResponse(json.dumps({
        'id': profile_model.id,
        'first_name': profile_model.first_name,
        'last_name': profile_model.last_name,
        'picture': profile_model.picture.url,
    }))


def define_user(request):
    user = request.user

    if not user.id:
        return HttpResponse(json.dumps({
            'id': 0,
            'first_name': '',
            'last_name': '',
            'picture': '',
        }))

    profile_model = models.ProfileModel.objects.get(id=user.id)

    return HttpResponse(json.dumps({
        'id': profile_model.id,
        'first_name': profile_model.first_name,
        'last_name': profile_model.last_name,
        'picture': profile_model.picture.url,
    }))


def account_logout(request):
    if request.user:
        login(request, request.user)

    return HttpResponse()


def account_register(request):
    if request.user:
        logout(request)

    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    picture = request.FILES['file']

    if User.objects.filter(username=username).exists():
        return HttpResponse('wrong')

    user = User.objects.create_user(username=username, password=password, email=email)
    data_profile = {
        'id': user.id,
        'first_name': first_name,
        'last_name': last_name,
    }
    profile_model = models.ProfileModel.objects.create(
        **data_profile,
        picture=picture
    )

    return HttpResponse(json.dumps({**data_profile, 'picture': profile_model.picture.url}))
