from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('packages/', views.getUserPackages),
    path('packages/<str:pk>', views.getPackage),
    path('currentUserPackages/<str:pk>', views.getUserPackages),
    path('currentStages/', views.getCurrentStages),
    path('packageStages/<str:pk>', views.getPackageStages),
    path('confirmPackage/<str:pk>', views.confirmPackage)
]