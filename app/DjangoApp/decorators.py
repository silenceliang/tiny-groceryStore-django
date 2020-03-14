from .models import Product, Order
from django.views.decorators.csrf import requires_csrf_token
from django.http import JsonResponse

import json, logging
from functools import wraps

def dummy_json(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.content_type == 'application/json':
            if request.body:
                request.json = json.loads(request.body)
            else:
                request.json = None
        return func(request, *args, **kwargs)
    return wrapper

def vip_required(func):
    @dummy_json
    @wraps(func)
    def wrapper(request, *args,**kargs):
        data = request.json
        p_obj = Product.objects.get(p_id=data['product_id'])
        p_obj.vip = bool(data['prod_vip'])

        if p_obj.vip and not data['vip']:
            logging.warning('You are not allowed to order this product.')
            return JsonResponse({'status':False, 'message':'You are not allowed to order this product.'}, status=201)
        else:
            return func(request)
    return wrapper

def qty_enough(func):
    @dummy_json
    @wraps(func)
    def wrapper(request, *args,**kargs):
        data = request.json
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
    
    return wrapper    

