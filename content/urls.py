from django.urls import path
from . import views


urlpatterns=[
    path('', views.home, name='home'),
    path('keywords/', views.get_keywords, name='keywords'),
    path('bigrams/', views.get_bigrams, name='bigrams'),
]