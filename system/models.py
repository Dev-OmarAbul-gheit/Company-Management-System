from django.db import models
from django.contrib.auth.models import AbstractUser
from django_fsm import FSMField, transition
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


class PerformanceReview(models.Model):
    STAGE_CHOICES = [
        ('pending_review', 'Pending Review'),
        ('review_scheduled', 'Review Scheduled'),
        ('feedback_provided', 'Feedback Provided'),
        ('under_approval', 'Under Approval'),
        ('review_approved', 'Review Approved'),
        ('review_rejected', 'Review Rejected'),
        ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_reviews')
    review_date = models.DateField(null = True, blank=True)
    feedback = models.TextField(blank=True, null=True)
    review_stage = FSMField(default='pending_review', choices=STAGE_CHOICES)

    @transition(field=review_stage, source='pending_review', target='review_scheduled')
    def schedule_review(self):
        pass  # Add logic for scheduling a review if necessary

    @transition(field=review_stage, source='review_scheduled', target='feedback_provided')
    def provide_feedback(self, feedback):
        self.feedback = feedback

    @transition(field=review_stage, source='feedback_provided', target='under_approval')
    def submit_for_approval(self):
        pass  # Additional logic for manager notifications can be added here

    @transition(field=review_stage, source='under_approval', target='review_approved')
    def approve_review(self):
        pass  # Logic for approving a review

    @transition(field=review_stage, source='under_approval', target='review_rejected')
    def reject_review(self):
        pass  # Logic for rejecting a review

    @transition(field=review_stage, source='review_rejected', target='feedback_provided')
    def resubmit_feedback(self, feedback):
        self.feedback = feedback

    def __str__(self) -> str:
        return f"Performance Review for {self.employee.name} ({self.review_stage})"