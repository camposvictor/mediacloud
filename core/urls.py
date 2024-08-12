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
    path('edit-video/<int:id>', views.edit_video_view, name='edit-video'),
    path('images/', views.ImageView.as_view(), name='images'),
    path('edit-image/<int:id>', views.edit_image_view, name='edit-image'),
    path('delete-image/<int:id>', views.delete_image, name='delete_image'),
    path('audios/', views.AudioView.as_view(), name='audios'),
    path('edit-audio/<int:id>', views.edit_audio_view, name='edit-audio'),
]
