from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    path('orders/', views.OrdersListView.as_view(), name='orders'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('masters/', views.MastersView.as_view(), name='masters'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('appointment/', views.AppointmentView.as_view(), name='appointment'),
    path('review/create/', views.ReviewCreateView.as_view(), name='create_review'),
    path('orders/create/', views.OrderCreateView.as_view(), name='create_order'),
    path('ajax/get_master_services/', __import__('core.ajax').ajax.get_master_services, name='get_master_services'),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)