from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def thanks(request):
    return render(request, 'thanks.html')

def orders(request):
    return render(request, 'orders.html')

def order_detail(request, order_id):
    return render(request, 'order_detail.html',  {"order_id": order_id})