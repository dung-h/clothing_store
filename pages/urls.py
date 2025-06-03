from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Trang chủ
    path('about/', views.about_view, name='about'),
    path('lookbook/', views.lookbook_view, name='lookbook'),
    path('contact/', views.contact_view, name='contact'),
]
