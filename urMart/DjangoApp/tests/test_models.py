from django.test import TestCase
from DjangoApp.models import Product
# Create your tests here

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test menthods
        Product.objects.create(p_id='0', s_pcs=0, price=0, s_id='0', vip=False)
    
    def test_p_id_label(self):
        product = Product.objects.get(p_id='0')
        field_label = product._meta.get_field('p_id').verbose_name
        self.assertEquals(field_label, 'p id')

    def test_s_pcs_label(self):
        product = Product.objects.get(p_id='0')
        field_label = product._meta.get_field('s_pcs').verbose_name
        self.assertEquals(field_label, 's pcs')

    def test_price_label(self):
        product = Product.objects.get(p_id='0')
        field_label = product._meta.get_field('price').verbose_name
        self.assertEquals(field_label, 'price')

    def test_s_id_label(self):
        product = Product.objects.get(p_id='0')
        field_label = product._meta.get_field('s_id').verbose_name
        self.assertEquals(field_label, 's id')

    def test_vip_label(self):
        product = Product.objects.get(p_id='0')
        field_label = product._meta.get_field('vip').verbose_name
        self.assertEquals(field_label, 'vip')

    def test_get_absolute_url(self):
        product = Product.objects.get(p_id='0')
        self.assertEquals(product.get_absolute_url(), '/add2order')
