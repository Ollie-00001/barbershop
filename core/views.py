from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Барбершоп')

def thanks(request):
    return HttpResponse('Ваша заявка принята!')

def orders(request):
    return HttpResponse('Список заявок')

def order_detail(request, order_id):
    return HttpResponse(f'Заявка № {order_id}')