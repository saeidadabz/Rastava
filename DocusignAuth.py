import jwt
import time
from docusign_esign import ApiClient
import requests
from Rastave import settings

def create_jwt_token():
    
    integration_key = settings.DOCUSIGN['INTEGRATION_KEY']
    user_id = settings.DOCUSIGN['ACCOUNT_ID']
    private_key = settings.DOCUSIGN['PRIVATE_KEY']  # کلید خصوصی خود را در فایل امن ذخیره کنید

    # ایجاد JWT Payload
    payload = {
        "iss": integration_key,
        "sub": user_id,
        "aud": "account-d.docusign.com",  # برای محیط تست
        "scope": "signature impersonation",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600  # مدت اعتبار 1 ساعت
    }

   
    jwt_token = jwt.encode(payload,private_key, algorithm="RS256")
    return jwt_token

def get_access_token():
    # JWT را ایجاد کنید
    jwt_token = create_jwt_token()

    # ارسال درخواست به DocuSign برای دریافت Access Token
    url = "https://account-d.docusign.com/oauth/token"
    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt_token
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        raise Exception(f"Error getting access token: {response.text}")