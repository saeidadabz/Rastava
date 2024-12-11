from django.urls import path
from django.contrib.auth.views import LoginView
from .views import RegisterView, login_view
from . import views

urlpatterns=[
    path('register/',RegisterView.as_view()),
    path('login/',login_view, name='login'),
    # path('get_token',views.create_jwt_token)

]