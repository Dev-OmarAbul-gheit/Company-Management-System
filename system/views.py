from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from .models import Company, Department, Employee, Project
from .serializers import CompanySerializer, DepartmentSerializer, EmployeeSerializer, ProjectSerializer


class CompanyViewSet(ListModelMixin,
                     RetrieveModelMixin,
                     GenericViewSet):
    
    queryset = Company.objects.prefetch_related("departments", "employees", "projects")
    serializer_class = CompanySerializer


class DepartmentViewSet(ListModelMixin,
                     RetrieveModelMixin,
                     GenericViewSet):
    
    queryset = Department.objects.select_related('company').prefetch_related('employees', 'projects')
    serializer_class = DepartmentSerializer


class EmployeeViewSet(ModelViewSet):
    http_method_names:list = ['get', 'post', 'patch', 'delete']
    queryset = Employee.objects.select_related('company', 'department')
    serializer_class = EmployeeSerializer


class ProjectViewSet(ModelViewSet):
    http_method_names:list = ['get', 'post', 'patch', 'delete']
    queryset = Project.objects.prefetch_related('employees')
    serializer_class = ProjectSerializer