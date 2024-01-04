from django.urls import path
from . import views

app_name = 'network'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('new_post/', views.new_post, name='new_post'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path("following/", views.following_view, name="following"),
    path("update_post/<int:post_id>/", views.update_post, name="update_post"),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('profile/<str:username>/follow/', views.follow_unfollow, name='follow_unfollow'),
]
