def menu_items(request):
    menu = [
        {'title': 'О нас', 'url': 'index'},
        {'title': 'Услуги', 'url': 'services'},
        {'title': 'Мастера', 'url': 'masters'},
        {'title': 'Запись', 'url': 'create_order'},
        {'title': 'Отзывы', 'url': 'create_review'},
    ]

    if request.user.is_authenticated and request.user.is_staff:
        menu.append({'title': 'Заявки', 'url': 'orders'})
        menu.append({'title': 'Админка', 'url': 'admin:index'})

    return {'menu_items': menu}