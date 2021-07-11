from django.shortcuts import HttpResponse
from django.http import response
#
from . import models
#
from account.models import ProfileModel
#
import json

# Create your views here.


def room_l(request):
    user = request.user
    room_name = request.GET['room_name']

    friend_id = f'{room_name}_'.replace(f'{user.id}_', '').replace('_', '')

    if not user:
        return HttpResponse(status=response.HttpResponseBadRequest)

    if not ProfileModel.objects.filter(id=friend_id).exists:
        return HttpResponse(status=response.HttpResponseBadRequest)

    room_model = models.Room.objects.get_or_create(name=room_name)
    c_count = request.GET['c_count']
    size = request.GET['size']

    message_model = models.Message.objects.filter(
        room_model=room_model.id
    ).order_by('-created_time')[c_count, c_count + size]

    return HttpResponse(json.dumps(message_model))


def message_l(request):
    user = request.user
    if not user:
        return HttpResponse(status=response.HttpResponseBadRequest)

    c_count = request.GET['c_count']
    size = request.GET['size']

    message_model = models.Message.objects.filter(
        room_model=models.Room.objects.get(name='world')
    ).order_by('-created_time')

    data = list(message_model[int(c_count):int(c_count) + int(size)].values())

    profile_model = ProfileModel.objects.all()
    result_data = []

    for item in data:
        c_user_id = item['profile_model_id']
        c_profile_model = profile_model.get(id=c_user_id)
        result_data.append({
            'id': c_user_id,
            'first_name': c_profile_model.first_name,
            'last_name': c_profile_model.last_name,
            'picture': c_profile_model.picture.url,
            'message': item['message'],
            'created_time': item['created_time'],
        })

    return response.JsonResponse({'data': result_data, 'count': message_model.count()}, safe=False)
