from django.urls import path
from . import views



app_name = "adminpanel" 

urlpatterns = [
    path('dashboard', views.dashboard, name='admin_dashboard'),

    # users
    path('users/', views.users_list, name='users'),
    
    # products
    path('products/', views.products_list, name='products'),

    # categories
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/edit/<int:id>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:id>/', views.category_delete, name='category_delete'),

    # vendors
    path("vendors/", views.vendors, name="vendors"),
    path("vendors/add/", views.vendor_add, name="vendor_add"),
    path("vendors/edit/<int:id>/", views.vendor_edit, name="vendor_edit"),
    path('vendors/delete/<int:id>/', views.category_delete, name='category_delete'),





]
