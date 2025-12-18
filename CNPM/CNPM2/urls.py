from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_item, name='add_item'),
    path('delete/<int:pk>/', views.delete_item, name='delete_item'),
    path('update/<int:pk>/', views.update_item, name='update_item'),
    path('import/create/', views.create_import_receipt, name='create_import_receipt'),
    path('import/process/', views.process_import_receipt, name='process_import_receipt'),
    path('export/create/', views.create_export_receipt, name='create_export_receipt'),
    path('export/process/', views.process_export_receipt, name='process_export_receipt'),
    path('product-detail-api/<int:pk>/', views.product_detail_api, name='product_detail_api'),
]