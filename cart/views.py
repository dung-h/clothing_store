from django.shortcuts import redirect, render, get_object_or_404
from products.models import Product
from django.contrib import messages
from django.http import JsonResponse
from .forms import CheckoutForm
from .models import Order, OrderItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required
import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render, get_object_or_404
from .models import Order
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'cart/admin_order_detail.html', {'order': order})

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'cart/order_history.html', {'orders': orders})

@staff_member_required
def admin_order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'cart/admin_orders.html', {'orders': orders})

def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
    return redirect('cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for product_id_str, quantity in cart.items():
        product = get_object_or_404(Product, pk=int(product_id_str))
        items.append({
            'product': product,
            'quantity': quantity
        })

    total_price = sum(float(item['product'].price) * int(item['quantity']) for item in items)


    return render(request, 'cart/cart_detail.html', {
    'cart_items': items,
    'total_price': total_price,
})


def cart_checkout(request):
    request.session['cart'] = {}
    messages.success(request, "Thanh toán thành công! Cảm ơn bạn đã mua hàng.")
    return redirect('cart_detail')

def cart_update(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                try:
                    product_id = key.split('_')[1]
                    quantity = int(value)
                    if quantity > 0:
                        cart[product_id] = quantity
                except ValueError:
                    continue

        request.session['cart'] = cart
        messages.success(request, "Đã cập nhật giỏ hàng.")
    return redirect('cart_detail')

def cart_update_ajax(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
            if quantity > 0:
                cart = request.session.get('cart', {})
                cart[product_id] = quantity
                request.session['cart'] = cart
                return JsonResponse({'success': True})
        except:
            pass
    return JsonResponse({'success': False}, status=400)



def checkout_view(request):
    logger.warning("=== Checkout view called ===")
    logger.warning(f"User authenticated: {request.user.is_authenticated}")
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "Giỏ hàng của bạn đang trống.")
        return redirect('/cart/')

    # Nếu người dùng đã đăng nhập, lấy thông tin từ User
    user = request.user if request.user.is_authenticated else None
    # print("Đã đăng nhập:", request.user.is_authenticated)
    # print("User:", request.user)
    logger.warning(f"Checkout called! Logged in? {request.user.is_authenticated} | User: {request.user}")

    # Tính tổng tiền và tạo đơn hàng
    total_price = 0
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        name=request.POST.get('name', 'Khách vãng lai'),
        address=request.POST.get('address', ''),
        phone=request.POST.get('phone', ''),
        note=request.POST.get('note', '')
    )


    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            quantity = int(quantity)
            total_price += float(product.price) * quantity
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )
        except Product.DoesNotExist:
            continue

    order.total_price = total_price
    order.save()
    if user and user.email:
        recipient = user.email
    # elif order.email:  # nếu sau này có form cho khách nhập email
    #     recipient = order.email
    else:
        recipient = None

    if recipient:
        send_mail(
            subject=f'Xác nhận đơn hàng #{order.id}',
            message=f'Cảm ơn {order.name}, đơn hàng của bạn đã được ghi nhận!',
            from_email=None,
            recipient_list=[recipient],
            fail_silently=True
        )
    # Xóa session giỏ hàng
    request.session['cart'] = {}

    messages.success(request, "Thanh toán thành công! Đơn hàng của bạn đã được ghi nhận.")
    return redirect('/cart/orders/')

def checkout_success(request):
    return render(request, 'cart/checkout_success.html')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'cart/my_orders.html', {'orders': orders})

