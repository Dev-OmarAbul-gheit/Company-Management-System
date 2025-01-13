from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_fsm_log.admin import StateLogInline
from .models import UserAccount, Company, Department, Employee, Project, PerformanceReview


admin.site.site_header = 'Company Management System'
admin.site.index_title = 'Admin'


@admin.register(UserAccount)
class UserAccountAdmin(UserAdmin):
    list_display = ['id', 'username', 'email', 'role', 'employee']
    search_fields = ['username', 'email']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('username', 'password1', 'password2', 'email', 'role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            
        }),
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'number_of_departments', 'number_of_employees', 'number_of_projects']
    search_fields = ['name__istartswith']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('departments', 'employees', 'projects')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name','company', 'number_of_employees', 'number_of_projects']
    search_fields = ['name__istartswith']
    list_select_related = ['company']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('employees', 'projects')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'mobile_number', 'address', 'position', 'department', 'company']
    search_fields = ['name__istartswith', 'email']
    list_select_related = ['department', 'company']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'department', 'company']
    search_fields = ['name__istartswith']
    list_select_related = ['department', 'company']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('employees')


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'review_stage', 'review_date')
    list_select_related = ['employee']
    inlines = [StateLogInline]