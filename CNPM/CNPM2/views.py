from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import InventoryItem

# 1. Trang chủ: Hiển thị danh sách sản phẩm
def home(request):
    items = InventoryItem.objects.all().order_by('-id')
    return render(request, 'CNPM2/home.html', {'items': items})

# 2. Thêm mới: Chỉ cho phép khi đã đăng nhập
@login_required(login_url='login')
def add_item(request):
    if request.method == "POST":
        InventoryItem.objects.create(
            name=request.POST.get('name'),
            sku=request.POST.get('sku'),
            category=request.POST.get('category'),
            price=request.POST.get('price', 0),
            quantity=request.POST.get('quantity', 1),
            mode=request.POST.get('mode'),
            image=request.FILES.get('image'),
        )
    return redirect('home')

# 3. Xóa sản phẩm: Dựa trên ID (pk) truyền từ URL
@login_required(login_url='login')
def delete_item(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    item.delete()
    return redirect('home')

# 4. Cập nhật sản phẩm: Nhận dữ liệu từ form Sửa gửi lên
@login_required(login_url='login')
def update_item(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == "POST":
        item.name = request.POST.get('name')
        item.sku = request.POST.get('sku')
        item.category = request.POST.get('category')
        item.price = request.POST.get('price', 0)
        item.quantity = request.POST.get('quantity', 1)
        # Không thay đổi mode (Loại phiếu) khi sửa để đảm bảo tính nhất quán
        item.save()
    return redirect('home')