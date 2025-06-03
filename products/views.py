from django.shortcuts import render, get_object_or_404
from .models import Product
from django.db.models import F
from django.utils import timezone
from django.core.paginator import Paginator

def product_list(request):
    product_list = Product.objects.all().order_by('-created_at')  # sắp xếp sản phẩm mới nhất lên đầu
    paginator = Paginator(product_list, 9)  # 9 sản phẩm mỗi trang

    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {'products': products})



def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_detail.html', {'product': product})
