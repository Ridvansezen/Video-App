from django.urls import path
from posts import views

app_name = "posts"

urlpatterns = [
    # Tür seçimi ile create view
    path("create/<str:post_type>/", views.create_post, name="create_post"),
    path("explore/", views.explore, name="explore"),
    path("user/<str:username>/", views.user_posts, name="user_posts"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/<int:pk>/like/", views.toggle_like, name="toggle_like"),
    path("post/<int:pk>/save/", views.toggle_save, name="toggle_save"),
]