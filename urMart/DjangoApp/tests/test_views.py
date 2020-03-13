from django.test import TestCase
from DjangoApp.models import Product, Order
from django.urls import reverse,reverse_lazy
from unittest.mock import patch

class ProductListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_prodct = 13
        for product_id in range(number_of_prodct):
            Product.objects.create(
                p_id=str(product_id),
                s_pcs=0,
                price=0,
                s_id=0,
                vip=False
            )
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('render-template'))
        self.assertEqual(response.status_code, 200)       
   
    # @patch('DjangoApp.decorators.qty_enough', lambda func: func)
    # def test_view_url_product_to_order(self):
    #     response = self.client.get(reverse('add-to-order'))
    #     self.assertEqual(response.status_code, 200)
        
    # @patch('DjangoApp.decorators.qty_enough', lambda func: func)
    # def test_view_url_delete_from_order(self):
    #     response = self.client.get(reverse('delete-from-order'))
    #     self.assertEqual(response.status_code, 200)
        
    def test_view_url_top_3_show(self):
        response = self.client.get(reverse_lazy('find-top3'))
        self.assertEqual(response.status_code, 200)
