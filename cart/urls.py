from django.urls import path
from . import views
from .views import order_history_view
from .views import admin_order_list
urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('update/', views.cart_update, name='cart_update'),
    path('ajax/update/', views.cart_update_ajax, name='cart_update_ajax'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('orders/', views.my_orders, name='my_orders'),
    path('history/', order_history_view, name='order_history'),
    path('admin/orders/', admin_order_list, name='admin_orders'),
    path('admin/orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),

]
