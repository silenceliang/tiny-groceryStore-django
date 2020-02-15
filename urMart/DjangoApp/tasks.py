from .models import Order
from django.db.models import Count,Sum, F

def totalGains():
    total = Order.objects.values('s_id').order_by('-total').annotate(total=Sum(F('price')*F('qty')))
    return list(total)
def totalSellQuantity():
    total = Order.objects.values('s_id').order_by('-total').annotate(total=Sum('qty'))
    return list(total)
def orderNum():
    total = Order.objects.values('s_id').order_by('-total').annotate(total=Count('s_id'))
    return list(total)
