from rest_framework import serializers
from .models import Company, Department, Employee, Project


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'number_of_departments', 'number_of_employees', 'number_of_projects']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'company','number_of_employees', 'number_of_projects']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'mobile_number', 'address', 'position', 'hired_on', 'days_employed', 'company', 'department']


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'employees', 'company', 'department']