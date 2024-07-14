from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),
    path('', views.dashboard, name='dashboard'),
]

