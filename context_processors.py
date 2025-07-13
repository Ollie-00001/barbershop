def menu_items(request):
    menu = [
        {'title': 'О нас', 'url': 'index'},
        {'title': 'Услуги', 'url': 'services'},
        {'title': 'Мастера', 'url': 'masters'},
        {'title': 'Запись', 'url': 'appointment'},
    ]

    if request.user.is_authenticated and request.user.is_staff:
        menu.append({'title': 'Заявки', 'url': 'orders'})
        menu.append({'title': 'Админка', 'url': 'admin:index'})

    return {'menu_items': menu}