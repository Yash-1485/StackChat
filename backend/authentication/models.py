from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # remove default username field
    email = models.EmailField(unique=True)
    fullName = models.CharField(max_length=100)
    bio = models.TextField(blank=True,default="")
    profilePic = models.URLField(blank=True,default="")
    location = models.CharField(max_length=100, blank=True, default="")
    isOnboarded = models.BooleanField(default=False)
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'   # use email to login
    REQUIRED_FIELDS = ['fullName']
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def match_password(self, raw_password):
        return self.check_password(raw_password)

    @classmethod
    def find_by_email(cls, email):
        return cls.objects.filter(email=email).first()

