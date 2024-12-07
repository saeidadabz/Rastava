from django.urls import path

from .views import RegisterView, login
from . import views

urlpatterns=[
    path('register/',RegisterView.as_view()),
    path('login/',login, name='login'),
    # path('get_token',views.create_jwt_token)

]