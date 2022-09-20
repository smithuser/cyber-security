from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class AppUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("email is required")
        if not username:
            raise ValueError("username is required")

        if not password:
            raise ValueError("password is required")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password = None):
        user = self.create_user(
            email = email,
            username= username,
            password= password
        )

        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class AppUser(AbstractBaseUser):
    email=models.EmailField(verbose_name='email address', max_length=60, unique=True)
    username = models.CharField(verbose_name='username', max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    modified_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    is_active = models.BooleanField(verbose_name='is_active', default=True)
    status=models.CharField(verbose_name='status', max_length=10, default='Active')
    suspension_expires = models.DateField(verbose_name='suspensions_expires', blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    failed_login_tries = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    objects = AppUserManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class BannedMac(models.Model):
    address = models.CharField(verbose_name='mac_address', max_length=32)

    def get_address(self):
        addy = self.address
        split_addy = addy.split('_')
        return ':'.join(split_addy)