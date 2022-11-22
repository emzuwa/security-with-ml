from django.contrib import admin
from django.urls import path
from .views import index_page, predict_malware, threats_list

urlpatterns = [
    path('',index_page),
    # path('', Prediction.as_view(), name = 'prediction')
    path('predict/', predict_malware),
    path('threats/', threats_list),
]

