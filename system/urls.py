from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CompanyViewSet, DepartmentViewSet,
                    EmployeeViewSet, ProjectViewSet,
                    UserRegisterViewSet, UserLoginViewSet
                )

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename= 'companies')
router.register(r'departments', DepartmentViewSet, basename='departments')
router.register(r'employees', EmployeeViewSet, basename='employees')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'register', UserRegisterViewSet, basename='register')
router.register(r'login', UserLoginViewSet, basename= 'login')


urlpatterns = [
    path('', include(router.urls)),
]