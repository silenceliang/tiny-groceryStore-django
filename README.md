# DjangoProject

## Screen Shot

![](https://i.imgur.com/IdO9OFh.png)


## Requirement
* python 3.6.8
* django 2.2.9
* django-q 1.1.0

## Usage

### 0) To begin using the virtual environment, it needs to be activated
```bash
source bin/activate
```

### 1) Synchronizes the database state with the current set of models and migrations
```bash
python manage.py migrate --run-syncdb

```
### 2) Start our django application
```bash
python manage.py runserver
```

## Tasks

### set your schedule in url `/Admin`


### Run django-q to schedule your task
```bash
python manage.py qcluster
```

## ORM design

### Product

| field | type |
| ------ | ------ |
| *product_id |Char |
| stock_pcs | Integer |
| price | Integer |
| shop_id | String |
| vip | [Boolean |

### Order

| field | type |
| ------ | ------ |
| *id |UUID |
| product_id | Char |
| qty | [Integer |
| price | Integer |
| shop_id | String |
| c_id | Char |

**Note:** `c_id` is Customer ID that record who orders the product.

## Decorator module

### 1. credential check

```python
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
``` 
### 2. stock quantity 
```python
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
```    

