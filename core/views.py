from django.shortcuts import render
from .data import masters, services, orders as orders_data

masters_by_id = {m["id"]: m["name"] for m in masters}

def index(request):
    return render(request, 'index.html', {
                  "masters": masters,
                  "services": services,
                  })

def thanks(request):
    return render(request, 'thanks.html')

def orders(request):
    orders_with_master = []
    for order in orders_data:
        order_copy = order.copy()
        order_copy["master_name"] = masters_by_id.get(order["master_id"], "Неизвестный мастер")
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