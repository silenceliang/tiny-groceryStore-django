from django.db import models
from django.urls import reverse
import uuid
# Create your models here.

class Product(models.Model):

    p_id = models.CharField(primary_key=True, unique=True, max_length=1)
    s_pcs = models.IntegerField()
    price = models.IntegerField()
    s_id = models.TextField()
    vip = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse('product-details')

    def __str__(self):
        return '%s' % (self.p_id)

class Order(models.Model):

    o_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    p_id = models.CharField(max_length=1)
    qty = models.IntegerField()
    price = models.IntegerField()
    s_id = models.TextField()
    c_id = models.CharField(max_length=10)

    def get_absolute_url(self):
        return reverse('order-details')

    def __str__(self):
        return '%s, %s' % (self.o_id, self.p_id)
