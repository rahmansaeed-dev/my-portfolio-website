from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, Group,Permission
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomModelGroups(models.Model):
    custom_model = models.ForeignKey('CustomModel', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class CustomModelUserPermissions(models.Model):
    custom_model = models.ForeignKey('CustomModel', on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

class CustomModel(AbstractUser):
    username = None
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=254, unique=True)
    phonenumber = models.CharField(max_length=15)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Custom user"
        verbose_name_plural = "Custom users"

    groups = models.ManyToManyField(
        Group,
        through=CustomModelGroups,
        related_name='custom_user_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        through=CustomModelUserPermissions,
        related_name='custom_user_permissions',
        blank=True,
    )

class Contact(models.Model):
    user = models.ForeignKey(CustomModel, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100,blank=True)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=254,blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name

