from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('thanks/', views.thanks, name='thanks'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('masters/', views.masters_view, name='masters'),
    path('services/', views.services_view, name='services'),
    path('appointment/', views.appointment, name='appointment'),
]