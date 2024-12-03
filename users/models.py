from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group, Permission


class CustomUserManager(BaseUserManager):


    #  Create our users with the email and no username
    def create_user(self, email, password, **extra_fields):

        #  Check the email as it is a required field
        if not email:
            raise ValueError('The Email must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email,password, **extra_fields)


class CustomUser(AbstractUser,PermissionsMixin):
    # Create our custom user model with no username
    username = None
    city = models.CharField(max_length=100,blank=True,null=True)
    state = models.CharField(max_length=100,blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True)

    #deal with reverse accessors that collide with the AbstractUser Model
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name='user permissions',
    )

    #Made the email unique in order to use it as the identifier
    email = models.EmailField(unique=True)

    # Specify that the email should be used as the new username field
    USERNAME_FIELD = 'email'

    # Added some required fields such as the fn, ln, pass
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    # point to our own manager - a manger is responsible for the creation,deletion and update of a model instance
    objects = CustomUserManager()

    # Tell django that once the str function is called to return email
    def __str__(self):
        return self.email