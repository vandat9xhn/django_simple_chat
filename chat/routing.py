from django.urls import path
#
from .consumers import ChatConsumer

#


url_patterns = [
    path('ws/chat/<slug:room_name>/', ChatConsumer.as_asgi()),
]
