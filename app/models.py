from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import timedelta
from django.utils import timezone

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, phone, city, password=None, **extra_fields):
        if not phone:
            raise ValueError('City or phone is wrong')

        
        user = self.model(phone=phone, password=None, city=city **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)

        return user
    
    def create_superuser(self, phone, city, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(phone=phone, password=password, city=city **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=50, unique=True)
    city = models.ForeignKey('City', on_delete=models.DO_NOTHING, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['city']


    def __str__(self) -> str:
        return self.phone
    
class City(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.name


class Profile(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    bio = models.TextField()
    image = models.ImageField(upload_to='user/')
    user_id = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.first_name
    

class ProfileImage(models.Model):
    image = models.ImageField(upload_to='profile-image')
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.profile_id.first_name
    

class ProfileVideo(models.Model):
    video = models.ImageField(upload_to='profile-video')
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.profile_id.first_name
    

class Favourite(models.Model):
    owner_id = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    profiles_id = models.ManyToManyField(Profile, related_name='profiles', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.owner_id.phone
    

class OneTimePassword(models.Model):
    user_id = models.OneToOneField(User, related_name='onetime', on_delete=models.CASCADE)
    otp = models.IntegerField()
    finish_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.finish_at = timezone.now() + timedelta(minutes=1)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.user_id.phone
