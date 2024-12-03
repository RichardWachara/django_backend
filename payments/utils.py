import requests
import base64
from datetime import datetime
from django.conf import settings

def get_access_token(consumer_key, consumer_secret):
    url = f"{settings.MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(consumer_key, consumer_secret))
    response.raise_for_status()  # Raise exception for failed requests
    return response.json().get("access_token")


def initiate_stk_push(phone_number, amount, account_reference, callback_url):

    # Generate access token
    access_token = get_access_token(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)


    url = f"{settings.MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest"
    headers = {'Authorization': f'Bearer {access_token}'}

    # Generate password
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(
        f"{settings.BUSINESS_SHORT_CODE}{settings.MPESA_PASSKEY}{timestamp}".encode()
    ).decode()

   
    # Prepare payload
    payload = {    
       "BusinessShortCode": settings.BUSINESS_SHORT_CODE,    
       "Password": password,    
       "Timestamp": timestamp,    
       "TransactionType": "CustomerPayBillOnline",    
       "Amount": int(amount),    
       "PartyA": phone_number,    
       "PartyB": settings.BUSINESS_SHORT_CODE,    
       "PhoneNumber": phone_number,    
       "CallBackURL": callback_url,    
       "AccountReference": account_reference,    
       "TransactionDesc": "Test"
    }

    # Send STK Push request
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()