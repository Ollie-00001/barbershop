from django.shortcuts import render, get_object_or_404
from .data import masters_list, services_list, orders as orders_data
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Q
from .models import Order, Master, Review

masters_by_id = {m["id"]: m["name"] for m in masters_list}

def is_staff_user(user):
    return user.is_staff

def index(request):
    masters = Master.objects.all()
    reviews = Review.objects.all()
    return render(request, 'index.html', {
        "masters": masters,
        "reviews": reviews
    })

def masters_view(request):
    return render(request, 'masters.html', {
                  "masters": masters_list,
                  })

def services_view(request):
    return render(request, 'services.html', {
                  "services": services_list,
                  })

def appointment(request):
    return render(request, 'appointment.html')

def thanks(request):
    return render(request, 'thanks.html')

@user_passes_test(is_staff_user)
def orders(request):
    orders_with_master = []
    for order in orders_data:
        order_copy = order.copy()
        order_copy["master_name"] = masters_by_id.get(order["master_id"], "Неизвестный мастер")
        order_copy["status_class"] = order_copy["status"].strip().lower()
        orders_with_master.append(order_copy)

    return render(request, "orders.html", {
        "orders": orders_with_master,
    })

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "order_detail.html", {"order": order})

@login_required
def orders(request):
    query = request.GET.get("q", "")
    search_name = request.GET.get("search_name", "on")
    search_phone = request.GET.get("search_phone")
    search_comment = request.GET.get("search_comment")
    search_master = request.GET.get("search_master")

    orders = Order.objects.all().order_by("-date_created")

    if query:
        q_filter = Q()
        if search_name:
            q_filter |= Q(client_name__icontains=query)
        if search_phone:
            q_filter |= Q(phone__icontains=query)
        if search_comment:
            q_filter |= Q(comment__icontains=query)
        if search_master:
            q_filter |= Q(master__name__icontains=query)
        orders = orders.filter(q_filter)

    return render(request, "orders.html", {"orders": orders})