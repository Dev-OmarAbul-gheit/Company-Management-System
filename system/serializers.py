from rest_framework import serializers
from .models import PerformanceReview

class PerformanceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceReview
        fields = ['id', 'employee', 'review_date', 'feedback', 'review_stage']
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import Company, Department, Employee, Project, UserAccount
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterSerializer(BaseUserCreateSerializer):
    username = serializers.CharField(max_length = 20, write_only = True)
    password = serializers.CharField(max_length = 50)
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['username', 'email', 'password']


class UserToken(serializers.Serializer):
    refersh_token = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)
    user_type = serializers.CharField(read_only=True)

    def create_user_token(self, user):
        refersh_token = RefreshToken.for_user(user)
        access_token = refersh_token.access_token
        return {
            "refersh_token": str(refersh_token),
            "access_token": str(access_token),
            "user_type": user.role,
        }


class UserLoginSerializer(UserToken, serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        if user := authenticate(email=email, password=password):
            return self.create_user_token(user)
        raise serializers.ValidationError("email or password wrong")


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