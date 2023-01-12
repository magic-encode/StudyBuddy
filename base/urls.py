from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path("login/", views.loginPage, name="login"),
    path("register/", views.registerPage, name="register"),
    path("logout/", views.logoutPage, name="logout"),
    
    path('room/<str:pk>/', views.room, name='room'),
    path('create_room/', views.create_room, name='create_room'),
    path('update_room/<str:pk>/', views.update_room, name='update_room'),
    path('delete_room/<str:pk>/', views.deleteRoom, name='delete_room'),
    
    path('delete-message/', views.deleteMessage, name='delete-message'),
]
