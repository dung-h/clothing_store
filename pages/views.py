from django.shortcuts import render, redirect
from django.contrib import messages

def about_view(request):
    return render(request, 'pages/about.html')

def lookbook_view(request):
    return render(request, 'pages/lookbook.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # (sau này sẽ gửi email hoặc lưu vào DB)
        messages.success(request, "Cảm ơn bạn đã liên hệ, chúng tôi sẽ phản hồi sớm!")
        return redirect('contact')
    return render(request, 'pages/contact.html')


def home_view(request):
    return render(request, 'pages/home.html')
