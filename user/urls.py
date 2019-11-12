from django.urls import path
from user import views

urlpatterns = [
    # 发送手机验证码
    path('phone_send_code/', views.phone_send_code),
    # 获取图形验证码
    path('captcha/', views.captcha),
    # 检查当前手机号是否已经注册
    path('check_is_register/', views.check_is_register),
    # 手机号注册
    path('phone_register/', views.phone_register),
    # 手机号、密码登陆
    path('login/', views.login),
]
