from django.db import models

class InventoryItem(models.Model):
    # Định nghĩa các loại phiếu
    MODE_CHOICES = [
        ('PRODUCT', 'Sản phẩm'),
        ('IMPORT', 'Nhập kho'),
        ('EXPORT', 'Xuất kho'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Tên mặt hàng")
    sku = models.CharField(max_length=50, unique=True, verbose_name="Mã SKU")
    category = models.CharField(max_length=100, verbose_name="Ngành hàng")
    price = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Giá bán")
    quantity = models.IntegerField(default=1, verbose_name="Số lượng")
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='PRODUCT')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.sku}"