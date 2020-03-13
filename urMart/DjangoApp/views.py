from .models import Product, Order
from .decorators import requires_csrf_token, vip_required, qty_enough
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.generic import TemplateView
from django.db.models import Sum, F
import os, csv, json, uuid, logging

class HomePageView(TemplateView):
    
    template_name = 'index.html'
    csv_storage = 'product.csv'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        try:
            with open(os.path.join(settings.STATIC_ROOT, self.csv_storage)) as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    try:
                        product = Product.objects.get(p_id=row[0])
                    
                    except Product.DoesNotExist:
                        Product.objects.create(
                            p_id=row[0],
                            s_pcs=int(row[1]),
                            price=int(row[2]),
                            s_id=row[3],
                            vip=0 if row[4]=='FALSE' else 1
                        )                   
        except FileExistsError as err:
            logging.error(err)
        else:
            context['allCategory'] =  Product.objects.all()
            context['allOrder'] =  Order.objects.all()
        finally:
            logging.info('Data setup complete')

        return context

@vip_required
@qty_enough
@requires_csrf_token
def add2order(request, notisify=False): 
    try:
        data = request.json
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

        res = model_to_dict(order)
        res['status'] = True
        return JsonResponse(res)
    except ObjectDoesNotExist:
        logging.error('Load database failed')

@qty_enough
@requires_csrf_token
def delFromOrder(request, notisify=False):
    try:
        data = request.json
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
    except ObjectDoesNotExist:
        logging.error('Load database failed')

@requires_csrf_token
def findTop3(request):
    top = Order.objects.values('p_id').order_by('p_id').annotate(total_sell=Sum('qty'))[:3]
    return JsonResponse({'results': list(top)})

def productDetails(request):
    return Product.objects.all()

def orderDetails(request):
    return Order.objects.all()

