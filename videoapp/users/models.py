from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinLengthValidator


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Kullanıcıların bir kullanıcı adı (username) olması gerekir")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser is_staff=True olmalı")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser is_superuser=True olmalı")

        return self.create_user(username, password, **extra_fields)

    
    
class UserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=16, unique=True, validators=[MinLengthValidator(4)], verbose_name="Kullanıcı adı")
    email = models.EmailField(blank=True, null=True, verbose_name="E-Posta")  # opsiyonel
    name = models.CharField(max_length=36, blank=True, null=True, validators=[MinLengthValidator(4)], verbose_name="isim, Soyisim")
    bio = models.TextField(max_length=350, blank=True, null=True, verbose_name="Biyografi")
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True, default="default.jpg" ,verbose_name="Profil resmi")
    joined_at = models.DateTimeField(auto_now_add=True)
    birth_date = models.DateField(blank=True, null=True) 

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"   # login için username
    REQUIRED_FIELDS = []          # ekstra alan yok

    objects = UserManager()

    def __str__(self):
        return self.username
