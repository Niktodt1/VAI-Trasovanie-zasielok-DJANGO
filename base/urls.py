from django.urls import path
from . import views
from django.templatetags.static import static # Not from django.conf.urls.static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name='register'),
    path('profile/<str:pk>', views.userProfile, name='userProfile'),
    path('updateUser/', views.updateUser, name='updateUser'),
    path('changePassword/', views.updateUser, name='changePassword'),

    path('', views.home, name="home"),
    path('newPackage/', views.newPackage, name="newPackage"),
    path('editPackage/<str:pk>/', views.editPackage, name="editPackage"),
    # TODO: filtrovanie podla obchodu na karte historia podla Django kurzu: 2:06:00
    path('history/', views.history, name="history"),

    path('deliveryCompanies/', views.deliveryCompanies, name="deliveryCompanies"),
    path('newDeliveryCompany/', views.createDeliveryCompany, name="newDeliveryCompany"),
    path('editDeliveryCompany/<str:pk>/', views.editDeliveryCompany, name='editDeliveryCompany'),
    path('deleteDeliveryCompany/<str:pk>/', views.deleteDeliveryCompany, name="deleteDeliveryCompany"),
    path('deliveryCompany/detail/<str:pk>/', views.deliveryCompanyDetail, name='deliveryCompanyDetail'),

    path('newCompany/', views.createCompany, name='createCompany'),
    path('editCompany/<str:pk>/', views.editCompany, name="editCompany"),
    path('deleteCompany/<str:pk>/', views.deleteCompany, name="deleteCompany"),
    path('company/detail/<str:pk>/', views.companyDetail, name='companyDetail'),

    path('contact/', views.contact, name="contact"),
    path('ajaxTest/', views.ajaxTesting, name='ajaxTest'),

    path('favicon.ico', RedirectView.as_view(url=static('favicon.ico'))),
]