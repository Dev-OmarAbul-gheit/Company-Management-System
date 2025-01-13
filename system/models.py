from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


class UserAccount(AbstractUser):
    MANAGER_ROLE: str = 'Manager'
    ADMIN_ROLE: str = 'Admin'
    EMPLOYEE_ROLE: str = 'Employee'
    ROLE_CHOICES: tuple = (
        (ADMIN_ROLE, 'Admin'),
        (MANAGER_ROLE, 'Manager'),
        (EMPLOYEE_ROLE, 'Employee'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=EMPLOYEE_ROLE)
    
    def __str__(self) -> str:
        return self.username
    
    class Meta:
        verbose_name:str = "User Account"
        verbose_name_plural:str = "User Accounts"


class Company(models.Model):
    name = models.CharField(max_length=255)
    
    @property
    def number_of_departments(self) -> int:
        return self.departments.count()

    @property
    def number_of_employees(self) -> int:
        return self.employees.count()

    @property
    def number_of_projects(self) -> int:
        return self.projects.count()

    def __str__(self) -> str:
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, related_name='departments', on_delete=models.CASCADE)

    @property
    def number_of_employees(self) -> int:
        return self.employees.count()

    @property
    def number_of_projects(self) -> int:
        return self.projects.count()

    def __str__(self) -> str:
        return self.name
    

class Employee(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    position = models.CharField(max_length=255)
    hired_on = models.DateField(null=True, blank=True)
    department = models.ForeignKey(Department, related_name='employees', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='employees' , on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    @property
    def days_employed(self) -> int | None:
        if self.hired_on:
            from datetime import date
            return (date.today() - self.hired_on).days
        return None


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    employees = models.ManyToManyField(Employee, related_name='projects')
    department = models.ForeignKey(Department, related_name='projects', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='projects', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name