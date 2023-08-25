from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
from accounts.managers import CustomUserManager
from django.utils.translation import gettext_lazy as _


GENDER_CHOICES = (
    ("male", "male"),
    ("female", "female"),
    
)
class User(AbstractBaseUser, PermissionsMixin):

    username = None
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    full_name = models.CharField(verbose_name=(_("Full name")), max_length=300)
    email = models.EmailField(verbose_name=(_("Email address")), unique=True)
    phone_number = models.CharField(max_length=45, unique=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField(verbose_name=_("Avatar"), upload_to="avatar/", blank=True, null=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def __str__(self):
        return str(self.email)
    
    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url 
        else:
            return None
    

class Jwt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access = models.CharField(max_length=1000)
    refresh = models.CharField(max_length=1000)
    refresh_expiry = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=24))

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return str(self.user.email)


