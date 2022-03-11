from django.db import models
from django.core.mail import send_mail
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager ,PermissionsMixin

class CustomUserManager(BaseUserManager):
    
    def create_superuser(self, email, user_name, password, **other_fields):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('superuser must be set to is_staff = true')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be set to is_superuser = true')

        return self.create_user(email,user_name,password, **other_fields)
    
    def create_user(self, email, user_name, password, **other_fields):
        if not email:
            raise ValueError(_('E-mail is mandatory'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user
        



class UserAcc(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('e-mail address'),unique=True)
    user_name = models.CharField(max_length=155, unique=True)
    first_name = models.CharField(max_length=155)
    about = models.TextField(blank=True, max_length=400)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    country = CountryField()
    phone_number = models.CharField(max_length=10, blank=True)
    address_line_one = models.CharField(max_length=155, blank=True)
    address_line_two = models.CharField(max_length=155, blank=True)
    city =  models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=20, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'admin@bookstore.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self) -> str:
        return self.user_name