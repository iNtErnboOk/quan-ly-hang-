from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_item, name='add_item'),
    path('delete/<int:pk>/', views.delete_item, name='delete_item'),
    path('update/<int:pk>/', views.update_item, name='update_item'),
]