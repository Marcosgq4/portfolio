from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('continue-as-guest/', views.continue_as_guest, name='continue_as_guest'),
    path('send_contact_email/', views.send_contact_email, name='send_contact_email'),
]