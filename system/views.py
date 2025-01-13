from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Company, Department, Employee, Project, UserAccount, PerformanceReview
from .permissions import IsAdmin, IsManager, IsEmployee
from .serializers import (CompanySerializer, DepartmentSerializer,
                          EmployeeSerializer, ProjectSerializer,
                          UserRegisterSerializer, UserLoginSerializer,
                          PerformanceReviewSerializer
                        )


class UserRegisterViewSet(CreateModelMixin,
                        GenericViewSet):
    queryset = UserAccount.objects.all()
    serializer_class  = UserRegisterSerializer
    permission_classes = [IsAuthenticated ,IsAdmin]


class UserLoginViewSet(CreateModelMixin, GenericViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]


class CompanyViewSet(ListModelMixin,
                     RetrieveModelMixin,
                     GenericViewSet):
    
    serializer_class = CompanySerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Company.objects.prefetch_related("departments", "employees", "projects")

        elif user.role == 'Manager':
            if Employee.objects.filter(account_id = self.request.user.id).exists():
                company_id = Employee.objects.get(account_id = self.request.user.id).company.id
                return Company.objects.prefetch_related("departments", "employees", "projects").filter(id=company_id)

    def get_permissions(self):
        if self.request.user.is_authenticated:

            if self.request.user.role == 'Admin':
                return [IsAdmin()]

            elif self.request.user.role == 'Manager':
                return [IsManager(['list'])]
            
            elif self.request.user.role == 'Employee':
                return [IsEmployee()]
        
        return [IsAuthenticated()]


class DepartmentViewSet(ListModelMixin,
                        RetrieveModelMixin,
                        GenericViewSet):
    
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Department.objects.select_related('company').prefetch_related('employees', 'projects')

        elif user.role == 'Manager':
            if Employee.objects.filter(account_id = self.request.user.id).exists():
                department_id = Employee.objects.get(account_id = self.request.user.id).department.id
                return Department.objects.select_related('company').prefetch_related('employees', 'projects').filter(id=department_id)

    def get_permissions(self):
        if self.request.user.is_authenticated:

            if self.request.user.role == 'Admin':
                return [IsAdmin()]

            elif self.request.user.role == 'Manager':
                return [IsManager(['list'])]
            
            elif self.request.user.role == 'Employee':
                return [IsEmployee()]
        
        return [IsAuthenticated()]
    

class EmployeeViewSet(ModelViewSet):
    http_method_names:list = ['get', 'post', 'patch', 'delete']
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Employee.objects.select_related('company', 'department', 'account')

        elif user.role == 'Manager':
            if Employee.objects.filter(account_id = self.request.user.id).exists():
                company_id = Employee.objects.get(account_id = self.request.user.id).company.id
                department_id = Employee.objects.get(account_id = self.request.user.id).department.id
                return Employee.objects.select_related('company', 'department').filter(company = company_id, department=department_id)

        elif user.role == 'Employee':
            if Employee.objects.filter(account_id = self.request.user.id).exists():
                employee_id = Employee.objects.get(account_id = self.request.user.id).id
                return Employee.objects.select_related('company', 'department').filter(id = employee_id)


    def get_permissions(self):
        if self.request.user.is_authenticated:

            if self.request.user.role == 'Admin':
                return [IsAdmin()]

            elif self.request.user.role == 'Manager':
                return [IsManager(['list', 'create', 'retrieve', 'partial_update', 'destroy'])]
            
            elif self.request.user.role == 'Employee':
                return [IsEmployee(['list'])]
        
        return [IsAuthenticated()]


class ProjectViewSet(ModelViewSet):
    http_method_names:list = ['get', 'post', 'patch', 'delete']
    queryset = Project.objects.prefetch_related('employees')
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Project.objects.prefetch_related('employees')

        elif user.role == 'Manager':
            if Employee.objects.filter(account_id = self.request.user.id).exists():
                company_id = Employee.objects.get(account_id = self.request.user.id).company.id
                department_id = Employee.objects.get(account_id = self.request.user.id).department.id
                return Project.objects.prefetch_related('employees').filter(company = company_id, department=department_id)

        elif user.role == 'Employee':
            if Employee.objects.filter(account_id = self.request.user.id).exists():
                employee_id = Employee.objects.get(account_id = self.request.user.id).id
                return Project.objects.prefetch_related('employees').filter(employees__id=employee_id)

    def get_permissions(self):
        if self.request.user.is_authenticated:

            if self.request.user.role == 'Admin':
                return [IsAdmin()]

            elif self.request.user.role == 'Manager':
                return [IsManager(['list', 'create', 'retrieve', 'partial_update', 'destroy'])]
            
            elif self.request.user.role == 'Employee':
                return [IsEmployee(['list'])] 
        
        return [IsAuthenticated()]
    

class PerformanceReviewViewSet(ModelViewSet):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer

    @action(detail=True, methods=['post'])
    def transition(self, request, pk=None):
        review = self.get_object()
        transition = request.data.get('transition')
        
        try:
            if transition == 'schedule_review':
                review.schedule_review()
            elif transition == 'provide_feedback':
                feedback = request.data.get('feedback')
                review.provide_feedback(feedback)
            elif transition == 'submit_for_approval':
                review.submit_for_approval()
            elif transition == 'approve_review':
                review.approve_review()
            elif transition == 'reject_review':
                review.reject_review()
            elif transition == 'resubmit_feedback':
                feedback = request.data.get('feedback')
                review.resubmit_feedback(feedback)
            else:
                return Response({'error': 'Invalid transition'}, status=status.HTTP_400_BAD_REQUEST)
            
            review.save()
            return Response({'status': 'Transition successful', 'state': review.state}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)