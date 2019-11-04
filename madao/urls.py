from django.urls import path, include

urlpatterns = [
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('tweet/', include(('tweet.urls', 'tweet'), namespace='tweet')),
]
