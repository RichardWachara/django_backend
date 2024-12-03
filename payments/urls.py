from django.urls import path
from .views import InitiatePaymentView, VerifyCallbackView



urlpatterns = [
    path('initiate-payment/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('verify-callback/', VerifyCallbackView.as_view(), name='verify-callback'),
]