
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.newPost, name="newPost"),
    path('like/<int:post_id>/', views.like_post, name='like'),
    path('dislike/<int:post_id>/', views.dislike_post, name='dislike'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('following', views.following, name="following")
]
