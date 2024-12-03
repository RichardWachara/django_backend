from django.utils import timezone 
import threading
from rest_framework.views import APIView
from .utils import initiate_stk_push
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from .models import Payment
from django.conf import settings

class InitiatePaymentView(APIView):
    def post(self, request):
        """
        Initiates an STK Push to the user's phone.
        """
        phone_number = request.data.get('phone_number')
        amount = request.data.get('amount')

        if not phone_number or not amount:
            return Response({"error": "Phone number and amount are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Save a pending payment record
        payment = Payment.objects.create(phone_number=phone_number, amount=amount)

        try:
            # Initiate STK Push
            callback_url = settings.MPESA_CALLBACK_URL
            response = initiate_stk_push(phone_number, amount, f"Payment-{payment.id}", callback_url)
            return Response({"message": "STK Push initiated.", "response": response}, status=status.HTTP_200_OK)
        
        except Exception as e:
            payment.status = "FAILED"
            payment.save()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



        
class VerifyCallbackView(APIView):
    post_event = threading.Event()
    last_response = None

    def post(self, request):
        """
        Handles payment verification callbacks from Daraja.
        """
        print('There is a callback')
        data = request.data
        body = data.get('Body', {}).get('stkCallback', {})
        print(f"Body: {body}")

        result_code = body.get('ResultCode')
        result_desc = body.get('ResultDesc')
        metadata = body.get('CallbackMetadata', {}).get('Item', [])
        print()
        print(f"MetaData: {metadata}")
        transaction_id = None
        phone_number = None
        amount = None

        for item in metadata:
            if item['Name'] == 'MpesaReceiptNumber':
                transaction_id = item['Value']
            elif item['Name'] == 'PhoneNumber':
                phone_number = item['Value']
            elif item['Name'] == 'Amount':
                amount = item['Value']

        if result_code == 0:  # Payment successful
            payment = get_object_or_404(Payment, phone_number=phone_number, amount=amount, status='PENDING')
            payment.transaction_id = transaction_id
            payment.status = 'COMPLETED'
            payment.verified = True
            payment.payment_time = timezone.now()
            payment.save()

        else:
            # Update payment as failed
            payment = get_object_or_404(Payment, phone_number=phone_number, amount=amount, status='PENDING')
            payment.status = 'FAILED'
            payment.save()

        self.last_response = {"message": result_desc,"status": "SUCCESS" if result_code == 0 else "FAILED"}
        self.post_event.set() # Notify that the POST request has completed
        return Response(self.last_response, status=status.HTTP_200_OK)
    
    def get(self, request):
        phone_number = request.query_params.get('phone_number')
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        payment_status = get_object_or_404(Payment, phone_number=phone_number)
        return Response({"status": payment_status.status, "message": payment_status.message}, status=status.HTTP_200_OK)
    
