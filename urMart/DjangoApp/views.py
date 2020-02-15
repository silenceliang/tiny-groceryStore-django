from django.shortcuts import render
from django.conf import settings
from .models import Product, Order
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
# from django.core.serializers import serialize
# from django.contrib.auth.decorators import user_passes_test
from django.forms.models import model_to_dict
from django.views.decorators.csrf import requires_csrf_token
from django.db.models import Count,Sum, F
from django_q.tasks import async_task
import os, csv, json, uuid,logging
import functools

# Welcome mail with follow up example
from datetime import timedelta
from django.utils import timezone
from django_q.tasks import async_task, schedule

def vip_required(func):
    @functools.wraps(func)
    def wrap(request, *args,**kargs):
        data = json.loads(request.body.decode()) # order data
        p_obj = Product.objects.get(p_id=data['product_id'])
        p_obj.vip = bool(data['prod_vip'])

        if p_obj.vip and not data['vip']:
            logging.warning('You are not allowed to order this product.')
            return JsonResponse({'status':False, 'message':'You are not allowed to order this product.'}, status=201)
        else:
            return func(request)
    return wrap

def qty_enough(func):
    @functools.wraps(func)
    def wrap(request, *args,**kargs):
        data = json.loads(request.body.decode())
        p_obj = Product.objects.get(p_id=data['product_id'])
        notisify = False
        actions = data['action']
        # Stock from zero to n.
        if actions=='del' and p_obj.s_pcs==0 and int(data['qty'])>0:
            logging.warning('Enter the goods.')
            notisify = True
   
        # Not enough stock.
        if actions=='add' and p_obj.s_pcs < int(data['qty']):
            logging.warning('There is out of stock.')
            return JsonResponse({'status':False, 'message':'There is out of stock.'}, status=201)
        return func(request,notisify=notisify)
    
    return wrap    

@requires_csrf_token
def index(request):
    # read the given csv file.
    with open(os.path.join(settings.STATIC_ROOT,'product.csv')) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            try:
                product = Product.objects.get(p_id=row[0])
            except Product.DoesNotExist:
                created = Product.objects.create(
                    p_id=row[0],
                    s_pcs=int(row[1]),
                    price=int(row[2]),
                    s_id=row[3],
                    vip=0 if row[4]=='FALSE' else 1
                )                   
        allCategory = Product.objects.all()
        allOrder = Order.objects.all()

    return render(request, 'index.html', {
        'allCategory': allCategory,
        'allOrder':allOrder})

@vip_required
@qty_enough
@requires_csrf_token
def add2order(request,notisify=False):
    data = json.loads(request.body.decode())
    p_obj = Product.objects.get(p_id=data['product_id'])
    p_obj.s_pcs -= int(data['qty'])
    p_obj.save()

    order = Order(
        p_id=data['product_id'],
        qty=data['qty'],
        price=p_obj.price,
        s_id=p_obj.s_id,
        c_id=data['customer_id'])
    order.save()

    # --- client View ---
    # singleCustomerOrder = Ordedata.objects.filter(c_id=data['customer_id'])
    # for singleOrder in singleCdatastomerOrder:
    #     print(singleOrder)
    # return_order = serialize('json', order)

    res = model_to_dict(order)
    res['status'] = True
    
    return JsonResponse(res)

@qty_enough
@requires_csrf_token
def delFromOrder(request, notisify=False):
    data = json.loads(request.body.decode())
    # true stock
    o_obj = Order.objects.get(o_id=uuid.UUID(data['o_id']))

    data = {
        'status': True,
        'p_id': o_obj.p_id,
        'qty': o_obj.qty,
        'notice': notisify
    }
    # update current product quantity.
    p_obj = Product.objects.get(p_id=data['p_id'])
    p_obj.s_pcs += data['qty']
    p_obj.save()
    # delete this order.
    o_obj.delete()

    return JsonResponse(data)


@requires_csrf_token
def findTop3(request):
    # schedule(func="totalGains()",schedule_type='O')
    # schedule(func="totalSellQuantity()",schedule_type='O')
    # schedule(func="orderNum()",schedule_type='O')   
    
    top = Order.objects.values('p_id').order_by('p_id').annotate(total_sell=Sum('qty'))[:3]
    return JsonResponse({'results': list(top)})