from django.urls import path

from common import views

urlpatterns = [
    # 新添栏目
    path('add_column/', views.add_column),
    # 显示所有栏目，不分等级
    path('get_column_all/', views.get_column_all),
    # 显示一级栏目，将其余子栏目加入到child中
    path('get_one_column/', views.get_one_column),
]
