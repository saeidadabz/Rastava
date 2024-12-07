from django.urls import path
from .views import create_contract , sender_view

urlpatterns = [
    path('send-contract/', create_contract, name='send_contract'),
    path('sender-view/<str:envelope_id>/', sender_view, name='sender_view')
]