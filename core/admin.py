from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Master, Service, Review, Order

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'experience', 'is_active', 'display_services')
    search_fields = ('name', 'phone')
    list_filter = ('is_active', 'services')
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'photo', 'phone', 'address', 'experience', 'services', 'is_active')
        }),
    )

    def display_services(self, obj):
        return ", ".join([service.name for service in obj.services.all()])
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
    fieldsets = (
        (None, {
            'fields': ('text', 'client_name', 'master', 'photo', 'rating', 'is_published')
        }),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phone', 'status', 'appointment_date', 'date_created', 'master', 'display_services_admin')
    search_fields = ('client_name', 'phone', 'master__name')
    list_filter = ('status', 'master')
    ordering = ('-date_created',)
    fieldsets = (
        (None, {
            'fields': ('client_name', 'phone', 'comment', 'status', 'appointment_date', 'master', 'services')
        }),
    )
    filter_horizontal = ('services',)
    readonly_fields = ('date_created', 'date_updated')
    date_hierarchy = 'date_created'
    actions = ['mark_as_completed', 'mark_as_canceled']

    def display_services_admin(self, obj):
        return obj.display_services
    display_services_admin.short_description = "Услуги клиента"

    class Meta:
        ordering = ['-date_created']

    @admin.action(description="Отметить как выполненные")
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f"{updated} заказ(ов) отмечено как выполненные.")

    @admin.action(description="Отметить как отмененные")
    def mark_as_canceled(self, request, queryset):
        updated = queryset.update(status='canceled')
        self.message_user(request, f"{updated} заказ(ов) отмечено как отмененные.")
