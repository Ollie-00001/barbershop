from decimal import Decimal
from datetime import datetime, date, timedelta

from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Master, Service, Review, Order

admin.site.site_header = 'Панель управления барбершопа'
admin.site.index_title = 'Администрирование'
admin.site.site_title = 'Барбершоп "Скаттер" - Админка'

class OrderServiceInline(admin.TabularInline):
    model = Order.services.through
    extra = 1
    verbose_name = "Услуга в заказе"
    verbose_name_plural = "Услуги в заказе"

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('client_name', 'rating', 'text', 'photo', 'is_published', 'created_at')

class AppointmentDateFilter(admin.SimpleListFilter):
    title = _('Дата записи')
    parameter_name = 'appointment_date_filter'

    def lookups(self, request, model_admin):
        return (
            ('today', _('Сегодня')),
            ('tomorrow', _('Завтра')),
            ('this_week', _('На этой неделе')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset
        tznow = timezone.localtime(timezone.now())
        today = tznow.date()
        if value == 'today':
            start = datetime.combine(today, datetime.min.time()).replace(tzinfo=tznow.tzinfo)
            end = datetime.combine(today, datetime.max.time()).replace(tzinfo=tznow.tzinfo)
            return queryset.filter(appointment_date__range=(start, end))
        if value == 'tomorrow':
            tomorrow = today + timedelta(days=1)
            start = datetime.combine(tomorrow, datetime.min.time()).replace(tzinfo=tznow.tzinfo)
            end = datetime.combine(tomorrow, datetime.max.time()).replace(tzinfo=tznow.tzinfo)
            return queryset.filter(appointment_date__range=(start, end))
        if value == 'this_week':
            # неделя: от сегодня до конца недели (воскресенье)
            # вычислим конец недели (включительно)
            weekday = today.weekday()  # 0 = Mon ... 6 = Sun
            days_left = 6 - weekday
            end_day = today + timedelta(days=days_left)
            start = datetime.combine(today, datetime.min.time()).replace(tzinfo=tznow.tzinfo)
            end = datetime.combine(end_day, datetime.max.time()).replace(tzinfo=tznow.tzinfo)
            return queryset.filter(appointment_date__range=(start, end))
        return queryset

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'experience', 'is_active', 'services_count', 'display_services')
    search_fields = ('name',)
    list_filter = ('is_active', 'services')
    ordering = ('name',)
    inlines = (ReviewInline,)
    fieldsets = (
        (None, {
            'fields': ('name', 'photo', 'phone', 'address', 'experience', 'services', 'is_active')
        }),
    )

    @admin.display(description='Кол-во услуг')
    def services_count(self, obj):
        return obj.services.count()

    def display_services(self, obj):
        return ", ".join([s.name for s in obj.services.all()])
    display_services.short_description = "Услуги"

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_popular')
    search_fields = ('name',)
    list_filter = ('is_popular',)
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'duration', 'is_popular', 'image')
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'master', 'rating', 'created_at', 'is_published')
    search_fields = ('client_name', 'master__name')
    list_filter = ('is_published', 'rating')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('text', 'client_name', 'master', 'photo', 'rating', 'is_published')
        }),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'phone', 'master', 'status', 'appointment_date', 'total_price', 'display_services_admin')
    list_display_links = ('id', 'client_name')
    list_editable = ('status',)
    search_fields = ('client_name', 'phone', 'master__name')
    list_filter = ('status', 'master', AppointmentDateFilter)
    ordering = ('-date_created',)
    fieldsets = (
        (None, {
            'fields': ('client_name', 'phone', 'comment', 'status', 'appointment_date', 'master', 'services')
        }),
    )
    filter_horizontal = ('services',)
    readonly_fields = ('date_created', 'date_updated')
    date_hierarchy = 'date_created'
    inlines = (OrderServiceInline,)
    actions = ['mark_as_approved', 'mark_as_not_approved', 'mark_as_in_progress', 'mark_as_completed', 'mark_as_canceled']

    @admin.display(description="Услуги клиента")
    def display_services_admin(self, obj):
        return obj.display_services

    @admin.display(description="Сумма заказа")
    def total_price(self, obj):
        total = Decimal('0.00')
        for svc in obj.services.all():
            total += (svc.price or Decimal('0.00'))
        return f"{total:.2f}"

    @admin.action(description="Подтвердить")
    def mark_as_approved(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f"{updated} заказ(ов) отмечено как подтверждённые.")

    @admin.action(description="Отметить как новая")
    def mark_as_not_approved(self, request, queryset):
        updated = queryset.update(status='not_approved')
        self.message_user(request, f"{updated} заказ(ов) отмечено как новые.")

    @admin.action(description="Перевести в статус 'В работе'")
    def mark_as_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f"{updated} заказ(ов) переведено в 'В работе'.")

    @admin.action(description="Отметить как выполнённые")
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f"{updated} заказ(ов) отмечено как выполненные.")

    @admin.action(description="Отметить как отменённые")
    def mark_as_canceled(self, request, queryset):
        updated = queryset.update(status='canceled')
        self.message_user(request, f"{updated} заказ(ов) отмечено как отмененные.")
