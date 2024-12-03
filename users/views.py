from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .utils import send_registration_email
from django.conf import settings

# generate a tokenized url
from django.contrib.auth.tokens import default_token_generator

# Getting user object from the database or returning a NOT found when there is no such user
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer, TokenObtainPairSerializer

# The class view restricted to only post requests to register users
class RegisterView(APIView):
    http_method_names = ['post'] # Http request restrictions

    # Handles the post request and creates a user
    def post(self, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            created_user = get_user_model().objects.create_user(**serializer.validated_data, is_active=False)

            token = default_token_generator.make_token(created_user)
            verification_url = f"{settings.REACT_BASE_URL}/verify-email?token={token}&email={created_user.email}"

            # We want to send an email once our users regiser
            send_registration_email(created_user.email, created_user.first_name,verification_url)
            return Response({"message": "User Was created Successfully and an email sent"},status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})

# Email verification class view
class EmailVerification(APIView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        email = request.GET.get('email')

        if not token or not email:
            return Response({"error": "Missing token or email"}, status=HTTP_400_BAD_REQUEST)
        
        User_model = get_user_model()
        user = get_object_or_404(User_model, email=email)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully!"}, status=HTTP_200_OK)
        else:
            return Response({"error": "Invalid or expired token"}, status=HTTP_400_BAD_REQUEST)


#  overrides the TokenObtainPairView and provides it with our custom serializer that accepts an email instead of a username
class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer