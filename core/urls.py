from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('videos/', views.VideoView.as_view(), name='videos'),
    path('images/', views.ImageView.as_view(), name='images'),
    path('audios/', views.AudioView.as_view(), name='audios'),
#     path('media/<int:pk>/', views.view_media_view, name='view_media'),
#    ## path('media/<int:pk>/edit/', views.edit_media_view, name='edit_media'),
#     path('media/<int:pk>/delete/', views.delete_media_view, name='delete_media'),
#     path('search/', views.search_media_view, name='search_media'),
#     path('list/', views.list_media_view, name='list_media'),
]
