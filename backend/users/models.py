from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True, blank=False, region="KR")
    name = models.CharField(max_length=30, blank=False)
    is_active = models.BooleanField(
        default=False,
        help_text="관리자의 승인을 받아야 합니다.",
    )
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone_number"]

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customusers",
        related_query_name="customuser",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customusers",
        related_query_name="customuser",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.email
