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

def processingAll():
    a = totalGains()
    b = totalSellQuantity()
    c =orderNum()
    return "1. total sale gain: " + str(a)  + "\n" + \
            "2. total sale number: " + str(b) + "\n" + \
            "3. totoal order number: " + str(c) +"\n"