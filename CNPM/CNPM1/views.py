from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Kiểm tra tài khoản
        user = authenticate(request, username=username, password=password)

        if user is None:
            # Sai tài khoản hoặc mật khẩu
            return render(request, "CNPM1/login.html", {
                "error": "Tên đăng nhập hoặc mật khẩu không chính xác!"
            })

        # Đăng nhập thành công
        login(request, user)
        return redirect("home")

    return render(request, "CNPM1/login.html")

def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password-1")
        password2 = request.POST.get("password-2")

        # Kiểm tra ô trống
        if not username or not password1 or not password2:
            return render(request, "CNPM1/register.html", {
                "error": "Vui lòng nhập đầy đủ thông tin!"
            })

        # Kiểm tra mật khẩu khớp
        if password1 != password2:
            return render(request, "CNPM1/register.html", {
                "error": "Mật khẩu nhập lại không khớp!"
            })

        # Kiểm tra username đã tồn tại
        if User.objects.filter(username=username).exists():
            return render(request, "CNPM1/register.html", {
                "error": "Tên đăng nhập đã tồn tại!"
            })

        # Tạo user mới
        user = User.objects.create_user(username=username, password=password1)
        user.save()

        # Xong → chuyển về đăng nhập
        return redirect("login")

    return render(request, "CNPM1/register.html")

def logout_view(request):
    logout(request)
    return redirect('home')