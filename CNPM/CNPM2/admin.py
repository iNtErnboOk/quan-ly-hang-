from django.contrib import admin
from .models import InventoryItem, Supplier, ImportReceipt, ImportDetail

# Đăng ký các Model mới
admin.site.register(Supplier)
admin.site.register(ImportReceipt)
admin.site.register(ImportDetail)
admin.site.register(InventoryItem) # Chắc chắn là đã có

