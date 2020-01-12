from django.urls import path
from . import views
urlpatterns = [
    path('sentype/',views.sentype),
    path('textemotion/',views.textemotion),
    path('seetext/',views.seetext),
    path("",views.index),
]
