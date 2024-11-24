from django.urls import path
from . import views
from django.http import HttpResponse


urlpatterns = [
    path('',views.custom_login,name='custom_login'),
    path('logout/', views.custom_logout, name='logout'),
    path('organizations/', views.organization_list, name='organization_list'),
    path('users/<int:user_id>/assign-role/', views.assign_role, name='assign_role'),
    path('super_admin_dashboard/', views.super_admin_dashboard, name='super_admin_dashboard'),
    path('create_organization/', views.create_organization, name='create_organization'),
    path('edit_organization/<int:org_id>/', views.edit_organization, name='edit_organization'),
    path('delete_organization/<int:org_id>/', views.delete_organization, name='delete_organization'),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]
