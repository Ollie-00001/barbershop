from django.shortcuts import render
from .data import masters_list, services_list, orders as orders_data
from django.contrib.auth.decorators import user_passes_test

masters_by_id = {m["id"]: m["name"] for m in masters_list}

def is_staff_user(user):
    return user.is_staff

def index(request):
    return render(request, 'index.html')

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

def order_detail(request, order_id):
    order = next((o for o in orders_data if o["id"] == order_id), None)
    if not order:
        return render(request, "order_not_found.html", {"order_id": order_id}, status=404)

    order_copy = order.copy()
    order_copy["master_name"] = masters_by_id.get(order["master_id"], "Неизвестный мастер")

    return render(request, "order_detail.html", {
        "order": order_copy,
    })