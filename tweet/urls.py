# this ia the app url
from . import views
from django.urls import path


urlpatterns = [
    path('',views.tweet_list, name = 'tweet_list'),
    path('tweet/',views.tweet_list, name = 'tweet_list'),
    path('create/',views.tweet_create, name = 'tweet_create'),
    path('<int:tweet_id>/edit/',views.tweet_edit, name = 'tweet_edit'),
    path('<int:tweet_id>/delete/',views.tweet_delete, name = 'tweet_delete'),
    # path('register/',views.register, name = 'register'),
    path('registration/',views.registration , name ='reg'),
    path('logging/',views.user_login , name ='log'),
    path("user_logout" ,views.user_logout , name  = 'user_logout')
]
