from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('', views.profile, name='profile'),
    path('profile/<str:pk>/', views.user_profile, name="user-profile"),
]
