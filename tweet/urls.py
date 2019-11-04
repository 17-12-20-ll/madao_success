from django.urls import path

from tweet import views

urlpatterns = [
    # 添加推文
    path('add_tweet/', views.add_tweet),
    # 添加评论
    path('add_comment/', views.add_comment),
    # 添加二级评论
    path('add_second_comment/', views.add_second_comment),
    # 根据id查询单篇文章
    path('get_tweet/', views.get_tweet),

]
