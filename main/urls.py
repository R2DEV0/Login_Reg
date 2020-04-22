from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('new_user', views.new_user),
    path('login', views.login),
    path('profile/<int:user_id>', views.profile),
    path('logout', views.logout),
]