from django.db import models

# 1. Model Ngành hàng (Category)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Tên Ngành hàng")

    def __str__(self):
        return self.name

# 2. Model Sản phẩm (InventoryItem)
class InventoryItem(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    sku = models.CharField(max_length=50, unique=True, verbose_name="Mã SKU")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ngành hàng")
    price = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Giá bán (đ)")
    cost_price = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Giá vốn (đ)")
    quantity = models.IntegerField(default=0, verbose_name="Số lượng tồn kho")
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Hình ảnh")
    mode = models.CharField(max_length=20, default='PRODUCT') # Phân loại hiển thị

    def __str__(self):
        return f"{self.name} ({self.sku})"

# 3. Model Nhà cung cấp (Supplier)
class Supplier(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên nhà cung cấp")
    contact_info = models.TextField(blank=True, null=True, verbose_name="Thông tin liên hệ")

    def __str__(self):
        return self.name

# 4. Model Phiếu Nhập Kho (ImportReceipt)
class ImportReceipt(models.Model):
    receipt_code = models.CharField(max_length=50, unique=True, verbose_name="Mã Phiếu Nhập")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Nhà cung cấp")
    import_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=0, default=0)

    def __str__(self):
        return self.receipt_code

# 5. Chi tiết Phiếu Nhập (ImportDetail)
class ImportDetail(models.Model):
    receipt = models.ForeignKey(ImportReceipt, on_delete=models.CASCADE, related_name='details')
    item = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, verbose_name="Sản phẩm")
    imported_quantity = models.IntegerField()
    imported_price = models.DecimalField(max_digits=12, decimal_places=0)

# --- PHẦN MỚI: QUẢN LÝ XUẤT KHO ---

# 6. Model Phiếu Xuất Kho (ExportReceipt)
class ExportReceipt(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Chờ xử lý'),
        ('COMPLETED', 'Đã xuất kho'),
        ('CANCELLED', 'Đã hủy'),
    ]

    receipt_code = models.CharField(max_length=50, unique=True, verbose_name="Mã Phiếu Xuất")
    receiver_name = models.CharField(max_length=100, verbose_name="Người nhận hàng") # Tên người nhận
    export_date = models.DateTimeField(auto_now_add=True, verbose_name="Ngày xuất")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='PENDING', 
        verbose_name="Trạng thái"
    )
    total_amount = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name="Tổng giá trị xuất")
    note = models.TextField(blank=True, null=True, verbose_name="Ghi chú")

    def __str__(self):
        return f"{self.receipt_code} - {self.receiver_name}"

# 7. Chi tiết Phiếu Xuất (ExportDetail)
class ExportDetail(models.Model):
    receipt = models.ForeignKey(ExportReceipt, on_delete=models.CASCADE, related_name='export_details')
    item = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, verbose_name="Sản phẩm")
    exported_quantity = models.IntegerField(verbose_name="Số lượng xuất")
    exported_price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá xuất")

    def __str__(self):
        return f"Chi tiết {self.receipt.receipt_code} - {self.item.name}"