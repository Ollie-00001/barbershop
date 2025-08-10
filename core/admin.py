from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from .models import Master, Service, Review, Order


class ServiceInline(admin.TabularInline):
    model = Order.services.through
    extra = 1
    verbose_name = "Услуга"
    verbose_name_plural = "Услуги"


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ('created_at',)
    verbose_name = "Отзыв"
    verbose_name_plural = "Отзывы"


class AppointmentDateFilter(admin.SimpleListFilter):
    title = _("Дата записи")
    parameter_name = "appointment_date"

    def lookups(self, request, model_admin):
        return (
            ('today', _("Сегодня")),
            ('tomorrow', _("Завтра")),
            ('this_week', _("На этой неделе")),
        )

    def queryset(self, request, queryset):
        now = datetime.now()
        if self.value() == 'today':
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
            return queryset.filter(appointment_date__gte=start, appointment_date__lt=end)
        elif self.value() == 'tomorrow':
            start = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
            return queryset.filter(appointment_date__gte=start, appointment_date__lt=end)
        elif self.value() == 'this_week':
            start = now - timedelta(days=now.weekday())
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=7)
            return queryset.filter(appointment_date__gte=start, appointment_date__lt=end)
        return queryset


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'phone', 'master', 'status', 'appointment_date', 'total_price')
    search_fields = ('client_name', 'phone')
    list_filter = ('status', 'master', AppointmentDateFilter)
    ordering = ('-date_created',)
    list_editable = ('status',)
    actions = ['mark_as_approved', 'mark_as_canceled', 'mark_as_in_progress', 'mark_as_completed']
    inlines = [ServiceInline]

    fieldsets = (
        (None, {
            'fields': ('client_name', 'phone', 'comment', 'status', 'appointment_date', 'master', 'services')
        }),
    )
    filter_horizontal = ('services',)
    readonly_fields = ('date_created', 'date_updated')
    date_hierarchy = 'date_created'

    @admin.display(description="Общая стоимость услуг")
    def total_price(self, obj):
        return sum(service.price for service in obj.services.all())

    @admin.action(description="Отметить подтвержденным")
    def mark_as_approved(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f"{updated} заказ(ов) отмечено как подтверждённые.")

    @admin.action(description="Отметить отмененным")
    def mark_as_canceled(self, request, queryset):
        updated = queryset.update(status='canceled')
        self.message_user(request, f"{updated} заказ(ов) отмечено как отменённые.")

    @admin.action(description="Отметить как в обработке")
    def mark_as_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f"{updated} заказ(ов) отмечено как в работе.")

    @admin.action(description="Отметить выполненным")
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f"{updated} заказ(ов) отмечено как выполненные.")


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'experience', 'is_active', 'services_count')
    search_fields = ('name',)
    list_filter = ('is_active', 'services')
    inlines = [ReviewInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'photo', 'phone', 'address', 'experience', 'services', 'is_active')
        }),
    )

    @admin.display(description="Количество услуг")
    def services_count(self, obj):
        return obj.services.count()


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_popular')
    search_fields = ('name',)
    list_filter = ('is_popular',)
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
    fieldsets = (
        (None, {
            'fields': ('text', 'client_name', 'master', 'photo', 'rating', 'is_published')
        }),
    )
