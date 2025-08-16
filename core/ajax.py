from django.http import JsonResponse
from .models import Master

def get_master_services(request):
    master_id = request.GET.get('master_id')
    if not master_id:
        return JsonResponse({'services': []})
    try:
        master = Master.objects.get(pk=master_id)
        services = master.services.all()
        data = [{'id': s.id, 'name': s.name} for s in services]
        return JsonResponse({'services': data})
    except Master.DoesNotExist:
        return JsonResponse({'services': []})
