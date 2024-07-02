from django.urls import path
from base import views

urlpatterns = [
    path('', views.home_page, name="index"),
    path('explore/', views.explore_page, name="explore"),
]