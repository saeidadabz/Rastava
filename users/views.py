from django.shortcuts import render

from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate,login
from django.shortcuts import render , redirect
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm





import jwt
import time
from docusign_esign import ApiClient
import requests

from Rastave import settings
# Create your views here.

class RegisterView(CreateView):
    template_name='registeration/register.html'
    form_class=CustomUserCreationForm
    success_url=reverse_lazy('login')
    

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('contracts:create_contract')  # هدایت به صفحه ایجاد قرارداد
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

   





# def create_jwt_token():

#     integration_key = settings.DOCUSIGN['INTEGRATION_KEY']
#     user_id = settings.DOCUSIGN['ACCOUNT_ID']
#     private_key = settings.DOCUSIGN['PRIVATE_KEY']  # کلید خصوصی خود را در فایل امن ذخیره کنید

#     # ایجاد JWT Payload
#     payload = {
#         "iss": integration_key,
#         "sub": user_id,
#         "aud": "account-d.docusign.com",  # برای محیط تست
#         "scope": "signature impersonation",
#         "iat": int(time.time()),
#         "exp": int(time.time()) + 3600  # مدت اعتبار 1 ساعت
#     }


#     jwt_token = jwt.encode(payload,private_key, algorithm="RS256")
#     return jwt_token
