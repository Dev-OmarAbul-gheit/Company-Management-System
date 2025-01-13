from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


class UserAccount(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4)
    email = models.EmailField(unique=True)
    MANAGER_ROLE = 'Manager'
    ADMIN_ROLE = 'Admin'
    EMPLOYEE_ROLE = 'Employee'
    ROLE_CHOICES = (
        (ADMIN_ROLE, 'Admin'),
        (MANAGER_ROLE, 'Manager'),
        (EMPLOYEE_ROLE, 'Employee'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=EMPLOYEE_ROLE)
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "User Account"
        verbose_name_plural = "User Accounts"