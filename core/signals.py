from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Order
from .telegram import send_telegram_message

@receiver(m2m_changed, sender=Order.services.through)
def order_services_changed(sender, instance, action, **kwargs):
    if action == 'post_add':
        master = instance.master.name if instance.master else 'Not selected'
        services = ', '.join([s.name for s in instance.services.all()])
        text = (
            f"*У вас новый заказ!*\n"
            f"*Клиент:* {instance.client_name}\n"
            f"*Телефон:* {instance.phone}\n"
            f"*Мастер:* {master}\n"
            f"*Услуги:* {services}\n"
            f"*Дата:* {instance.appointment_date.strftime('%d.%m.%Y %H:%M')}"
        )
        send_telegram_message(text)
