from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Q, Sum
from .models import Order, Master, Review, Service

masters_by_id = {m.id: m.name for m in Master.objects.all()}
services_by_id = {s.id: s.name for s in Service.objects.all()}

def is_staff_user(user):
    return user.is_staff

def index(request):
    masters = Master.objects.all()
    reviews = Review.objects.select_related("master").all()
    return render(request, 'index.html', {
        "masters": masters,
        "reviews": reviews
    })

def masters_view(request):
    masters = Master.objects.all()
    return render(request, 'masters.html', {
                  "masters": masters,
                  })

def services_view(request):
    services = Service.objects.all()
    return render(request, 'services.html', {
                  "services": services,
                  })

def appointment(request):
    return render(request, 'appointment.html')

def thanks(request):
    return render(request, 'thanks.html')

def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.select_related("master").prefetch_related("services").annotate(total_price=Sum("services__price")),
        pk=pk
    )
    return render(request, "order_detail.html", {"order": order})

@login_required
def orders(request):
    query = request.GET.get("q", "")
    search_name = request.GET.get("search_name", "on")
    search_phone = request.GET.get("search_phone")
    search_comment = request.GET.get("search_comment")
    search_master = request.GET.get("search_master")

    orders = Order.objects.select_related("master").prefetch_related("services").order_by("-date_created")

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