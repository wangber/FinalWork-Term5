from django.urls import path
from . import views,view_mine
urlpatterns = [
    path('',views.index),
    path('register/',views.to_register),
    path('register_result/',views.register),
    path('login/',views.to_login),
    path('login_result/',views.login),
    path('givesen/',views.givesen),
    path('seeallsen/',views.allsen),
    path('aboutme/',view_mine.aboutme),
    path('alltype/',views.emotiontype),
]
