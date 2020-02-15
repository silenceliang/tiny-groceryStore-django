from django.db import models
import uuid
# Create your models here.
class Product(models.Model):

    p_id = models.CharField(primary_key=True, unique=True, max_length=1)
    s_pcs = models.IntegerField()
    price = models.IntegerField()
    s_id = models.TextField()
    vip = models.BooleanField(default=False)

class Order(models.Model):

    o_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    p_id = models.CharField(max_length=1)
    qty = models.IntegerField()
    price = models.IntegerField()
    s_id = models.TextField()
    c_id = models.CharField(max_length=10)
