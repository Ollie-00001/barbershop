
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db.models import Q, Sum
from .models import Order, Master, Review, Service
from .forms import ReviewForm, OrderForm
from django.contrib import messages

class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters'] = Master.objects.all()
        context['reviews'] = Review.objects.select_related('master').all()
        return context

class MastersView(TemplateView):
    template_name = 'masters.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters'] = Master.objects.all()
        return context

class ServicesView(TemplateView):
    template_name = 'services.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        return context

class AppointmentView(TemplateView):
    template_name = 'appointment.html'

class ThanksView(TemplateView):
    template_name = 'thanks.html'

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'create_review.html'
    success_url = reverse_lazy('thanks')
    def form_valid(self, form):
        messages.success(self.request, 'Ваш отзыв был успешно отправлен!')
        return super().form_valid(form)

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'create_order.html'
    success_url = reverse_lazy('thanks')
    def form_valid(self, form):
        messages.success(self.request, 'Ваша заявка принята!')
        return super().form_valid(form)

class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'
    def get_queryset(self):
        return Order.objects.select_related('master').prefetch_related('services').annotate(total_price=Sum('services__price'))

class OrdersListView(ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'
    ordering = ['-date_created']
    def get_queryset(self):
        queryset = super().get_queryset().select_related('master').prefetch_related('services')
        query = self.request.GET.get('q', '')
        search_name = self.request.GET.get('search_name', 'on')
        search_phone = self.request.GET.get('search_phone')
        search_comment = self.request.GET.get('search_comment')
        search_master = self.request.GET.get('search_master')
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
            queryset = queryset.filter(q_filter)
        return queryset