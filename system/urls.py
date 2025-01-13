from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, DepartmentViewSet, EmployeeViewSet, ProjectViewSet


router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'projects', ProjectViewSet)


urlpatterns = [
    path('', include(router.urls)),    
]