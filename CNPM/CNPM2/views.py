from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
import uuid
from django.db.models import Q 
from .models import InventoryItem, Supplier, ImportReceipt, ImportDetail, Category, ExportReceipt, ExportDetail
from django.views.decorators.cache import never_cache #
# KHU VỰC THAY ĐỔI: ĐẶT HẰNG SỐ MARKUP Ở ĐÂY
DEFAULT_MARKUP = 1.00 

def generate_new_sku(name):
    prefix = name[:4].upper()
    random_part = uuid.uuid4().hex[:8].upper()
    return f"SKU-{prefix}-{random_part}"

@never_cache
def home(request):
    items = InventoryItem.objects.all().order_by('-id') 
    all_categories = Category.objects.all() 
    selected_categories = request.GET.getlist('category_id')
    if selected_categories:
        items = items.filter(category__id__in=selected_categories)
    keyword = request.GET.get('q')
    if keyword:
        items = items.filter(Q(name__icontains=keyword) | Q(sku__icontains=keyword))
    
    # Sửa logic gửi selected_categories về template để checkbox giữ trạng thái tích
    return render(request, 'CNPM2/home.html', {
        'items': items, 
        'all_categories': all_categories, 
        'selected_categories': selected_categories, 
        'keyword': keyword
    })

# API lấy thông tin chi tiết sản phẩm
@login_required(login_url='login')
def product_detail_api(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    
    # Lấy lịch sử nhập/xuất gần nhất
    imports = ImportDetail.objects.filter(item=item).order_by('-receipt__import_date')[:5]
    exports = ExportDetail.objects.filter(item=item).order_by('-receipt__export_date')[:5]
    
    import_list = [f"<li>Ngày {i.receipt.import_date.strftime('%d/%m/%Y')}: Nhập {i.imported_quantity} (Giá: {i.imported_price:,}đ)</li>" for i in imports]
    export_list = [f"<li>Ngày {e.receipt.export_date.strftime('%d/%m/%Y')}: Xuất {e.exported_quantity} (Người nhận: {e.receipt.receiver_name})</li>" for e in exports]

    data = {
        'name': item.name,
        'sku': item.sku,
        'category': item.category.name if item.category else "N/A",
        'price': f"{item.price:,}đ",
        'cost_price': item.cost_price,
        'quantity': item.quantity,
        'image': item.image.url if item.image else None,
        'import_html': "".join(import_list) if import_list else "<li>Chưa có lịch sử nhập</li>",
        'export_html': "".join(export_list) if export_list else "<li>Chưa có lịch sử xuất</li>",
    }
    return JsonResponse(data)

@login_required(login_url='login')
def add_item(request):
    if request.method == "POST":
        category_id = request.POST.get('category') 
        name = request.POST.get('name')
        item_category_obj = get_object_or_404(Category, id=category_id) if category_id else None
        sku_code = generate_new_sku(name)
        InventoryItem.objects.create(
            name=name, sku=sku_code, category=item_category_obj, 
            price=request.POST.get('price', 0) or 0, quantity=request.POST.get('quantity', 1) or 0,
            mode='PRODUCT', image=request.FILES.get('image')
        )
    return redirect('home')

@login_required(login_url='login')
def delete_item(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    item.delete() 
    messages.warning(request, f"Đã xóa vĩnh viễn sản phẩm: {item.name}.")
    return redirect('home')

@login_required(login_url='login')
def update_item(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == "POST":
        item.name = request.POST.get('name')
        item.sku = request.POST.get('sku')
        item.price = request.POST.get('price', 0)
        item.quantity = request.POST.get('quantity', 1)
        if 'image' in request.FILES: item.image = request.FILES['image']
        category_id = request.POST.get('category')
        if category_id: item.category = get_object_or_404(Category, id=category_id)
        item.save()
    return redirect('home')

@login_required(login_url='login')
def create_import_receipt(request):
    suppliers = Supplier.objects.all()
    existing_items = InventoryItem.objects.all() 
    all_categories = Category.objects.all() 
    import_history = ImportReceipt.objects.all().prefetch_related('details__item', 'supplier').order_by('-import_date')
    unique_id = uuid.uuid4().hex[:6].upper()
    next_receipt_number = f"PN-{datetime.now().strftime('%Y%m%d')}-{unique_id}"
    context = {
        'suppliers': suppliers,
        'existing_items': existing_items,
        'next_receipt_number': next_receipt_number,
        'all_categories': all_categories,
        'import_history': import_history,
    }
    return render(request, 'CNPM2/create_import.html', context)

@login_required(login_url='login')
@transaction.atomic 
def process_import_receipt(request):
    if request.method == "POST":
        receipt_code = request.POST.get('receipt_code')
        supplier_id = request.POST.get('supplier')
        supplier = get_object_or_404(Supplier, id=supplier_id)
        new_receipt = ImportReceipt.objects.create(receipt_code=receipt_code, supplier=supplier)
        item_ids = request.POST.getlist('item_id')
        new_item_names = request.POST.getlist('new_item_name')
        imported_prices = request.POST.getlist('imported_price')
        imported_quantities = request.POST.getlist('imported_quantity')
        category_ids = request.POST.getlist('category_id') 
        total_receipt_amount = 0
        for i in range(len(imported_quantities)):
            item = None
            qty = int(imported_quantities[i] or 0)
            price = float(imported_prices[i] or 0)
            if item_ids[i] and item_ids[i].isdigit():
                item = get_object_or_404(InventoryItem, id=item_ids[i])
                item.quantity += qty
                item.cost_price = price 
                item.save()
            elif new_item_names[i] and new_item_names[i].strip() != "":
                category_id = category_ids[i] if i < len(category_ids) else None
                item_category_obj = get_object_or_404(Category, id=category_id)
                item = InventoryItem.objects.create(
                    name=new_item_names[i], sku=generate_new_sku(new_item_names[i]),
                    category=item_category_obj, price=price * DEFAULT_MARKUP,
                    cost_price=price, quantity=qty, mode='PRODUCT'
                )
            if item:
                ImportDetail.objects.create(receipt=new_receipt, item=item, imported_quantity=qty, imported_price=price)
                total_receipt_amount += qty * price
        new_receipt.total_amount = total_receipt_amount
        new_receipt.save()
        messages.success(request, f"Thành công: Đã lưu Phiếu Nhập {new_receipt.receipt_code}.")
    return redirect('home')

@login_required(login_url='login')
def create_export_receipt(request):
    existing_items = InventoryItem.objects.all()
    all_categories = Category.objects.all()
    export_history = ExportReceipt.objects.all().prefetch_related('export_details__item').order_by('-export_date')
    unique_id = uuid.uuid4().hex[:6].upper()
    export_prefix = f"PX-{datetime.now().strftime('%Y%m%d')}-{unique_id}"
    context = {
        'existing_items': existing_items, 'next_receipt_number': export_prefix, 
        'all_categories': all_categories, 'export_history': export_history,
    }
    return render(request, 'CNPM2/create_export.html', context)

@login_required(login_url='login')
@transaction.atomic
def process_export_receipt(request):
    if request.method == "POST":
        receipt_code = request.POST.get('receipt_code')
        receiver = request.POST.get('receiver_name')
        new_export = ExportReceipt.objects.create(receipt_code=receipt_code, receiver_name=receiver, note=request.POST.get('note', ''), status='COMPLETED')
        item_ids = request.POST.getlist('item_id')
        exported_quantities = request.POST.getlist('exported_quantity')
        total_export_amount = 0
        for i in range(len(exported_quantities)):
            if i < len(item_ids) and item_ids[i]:
                item = get_object_or_404(InventoryItem, id=item_ids[i])
                qty = int(exported_quantities[i])
                if item.quantity < qty:
                    transaction.set_rollback(True)
                    messages.error(request, f"Lỗi: '{item.name}' không đủ hàng.")
                    return redirect('create_export_receipt')
                item.quantity -= qty
                item.save()
                ExportDetail.objects.create(receipt=new_export, item=item, exported_quantity=qty, exported_price=item.price)
                total_export_amount += qty * item.price
        new_export.total_amount = total_export_amount
        new_export.save()
        messages.success(request, f"Thành công: Đã xuất kho phiếu {receipt_code}.")
    return redirect('home')