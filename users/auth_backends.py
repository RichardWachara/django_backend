from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# The ModelBackend handles the authentication processes using the authentication function
# The function uses a username and we want to override it to use an email
class EmailBackend(ModelBackend):

    # Override the authentication function
    def authenticate(self, request, **kwargs):

        # Load our AUTH_USER_MODEL
        UserModel = get_user_model()

        # try to check if the email provided matches the password provided and one stored in the database
        try:
            email = kwargs.get('email', None)
            if email is None:
                email = kwargs.get('username', None)
            user = UserModel.objects.get(email=email)
            if user.check_password(kwargs.get('password', None)):
                return user
        except UserModel.DoesNotExist:
            return None
        return None