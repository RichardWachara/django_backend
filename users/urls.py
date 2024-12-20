from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import EmailTokenObtainPairView, RegisterView, EmailVerification

urlpatterns = [
    path('register/', RegisterView.as_view(), name='token_obtain_pair'),
    path('verify-user/',EmailVerification.as_view(),name="verify-user"),
    path('token/obtain/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]