from django.conf.urls import url
from . import views,leida,citynum,emotionline,wordcloudimg,getcomment
from django.urls import path

urlpatterns = [
    path('getcomment/',getcomment.getcompage),
    path('index2/', views.IndexView.as_view(), name='index2'),
    url('leida/',leida.ChartView_leida.as_view(), name='index2'),
    url('citynumbar/',citynum.ChartView_citynumbar.as_view(), name='index2'),
    url('emotionline/',emotionline.ChartView_emotionline.as_view(),name="index2"),
    url("wordcloud/",wordcloudimg.CloudAPI),
    url("",views.index),
    
]
