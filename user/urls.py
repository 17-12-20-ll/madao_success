from django.urls import path
from user import views

urlpatterns = [
    path('phone_login/', views.phone_login),
]