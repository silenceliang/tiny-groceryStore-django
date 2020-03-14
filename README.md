# DjangoProject
This project simply demonstrates how to interact with database using django framework in python. Here we utilize ORM objects for CRUD in OOP way, and meanwhile we use the decorator-wrappers that make whole scripts more readable.

# Table Content
- [DjangoProject](#djangoproject)
  * [Dependencies](#dependencies)
  * [Requirements](#requirements)
  * [Snapshot](#snapshot)
  * [Usage](#usage)
    + [To begin using the virtual environment, it needs to be activated](#to-begin-using-the-virtual-environment--it-needs-to-be-activated)
    + [Synchronizes the database state with the current set of models and migrations](#synchronizes-the-database-state-with-the-current-set-of-models-and-migrations)
    + [Start our django application](#start-our-django-application)
  * [Task](#task)
    + [set your schedule in url `/Admin`](#set-your-schedule-in-url---admin-)
    + [Run django-q to schedule your task](#run-django-q-to-schedule-your-task)
  * [ORM Design](#orm-design)
    + [Product](#product)
    + [Order](#order)
  * [Decorator Wrapper](#decorator-design)
    + [1. credential check](#1-credential-check)
    + [2. stock quantity](#2-stock-quantity)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>



## Dependencies
* Python 3 (tested on python 3.6.8)

## Requirements
* django==2.2.9
* django-q==1.1.0
* django-bootstrap3==12.0.3
* django-bootstrap4==1.1.1
* django-tables2==2.2.1

## Snapshot
![](https://i.imgur.com/iDulepW.png)

## Usage

### To begin using the virtual environment, it needs to be activated
```bash
source bin/activate
```

### Synchronizes the database state with the current set of models and migrations
```bash
python manage.py migrate --run-syncdb

```
### Start our django application
```bash
python manage.py runserver
```

## Task

### set your schedule in url `/Admin`

### Run django-q to schedule your task
```bash
python manage.py qcluster
```

## ORM Design

### Product

| field | type |
| ------ | ------ |
| *product_id |Char |
| stock_pcs | Integer |
| price | Integer |
| shop_id | String |
| vip | Boolean |

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

## Decorator Wrapper

### credential check

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
### stock quantity 
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

