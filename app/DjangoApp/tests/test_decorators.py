from django.test import TestCase
from DjangoApp.decorators import requires_csrf_token, vip_required, qty_enough
from DjangoApp.models import Product, Order
from unittest.mock import Mock
from django.test import Client


# class TestVipRequired(TestCase):
#     def test_order_vip_required_without_vip(self):
#         def prepare_request_without_vip():
#             return HttpResponse({'product_id':'0',
#                     'prod_vip':True,
#                     'vip':False},
#                     content_type='application/json')
#         func = Mock()
#         decorated_func = vip_required(func)
#         request = prepare_request_without_vip()
#         response = decorated_func(request)
#         assert not func.called
    
#     def test_order_vip_required_with_vip(self):
#         def prepare_request_with_vip():
#             return {'product_id':'0',
#                     'prod_vip':True,
#                     'vip':True}
#         func = Mock()
#         decorated_func = vip_required(func)
#         request = prepare_request_with_vip()
#         response = decorated_func(request)
#         assert not func.called