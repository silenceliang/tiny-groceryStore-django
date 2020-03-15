# DjangoProject
This project simply demonstrates how to interact with database using django framework in python. Here we utilize ORM objects for CRUD in OOP way, and meanwhile we use the decorator-wrappers that make whole scripts more readable.

## Table Content

- [DjangoProject](#djangoproject)
  * [Dependencies](#dependencies)
  * [Requirements](#requirements)
  * [Snapshot](#snapshot)
  * [Usage](#usage)
    + [Synchronizes the database state with the current set of models and migrations](#synchronizes-the-database-state-with-the-current-set-of-models-and-migrations)
    + [Start our django application](#start-our-django-application)
    + [Run tests in django](#run-tests-in-django)
  * [Deployment](#deployment)
  * [Task](#task)
    + [set your schedule in url `/Admin`](#set-your-schedule-in-url---admin-)
    + [Run django-q to schedule your task](#run-django-q-to-schedule-your-task)
  * [ORM Design](#orm-design)
    + [Product](#product)
    + [Order](#order)
  * [Decorator Wrapper](#decorator-wrapper)
    + [vip credential](#vip-credential)
    + [stock quantity](#stock-quantity)

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

### Synchronizes the database state with the current set of models and migrations
```bash
python manage.py migrate --run-syncdb

```
### Start our django application
```bash
python manage.py runserver
```
### Run tests in django
```bash
python manage.py test
```

## Deployment

```bash
docker-compose up
```

## Task

### set your schedule in url `/Admin`

### Run django-q to schedule your task
```bash
python manage.py qcluster
```

## ORM Design

### Product

| field | description |
| ------ | ------ |
| *product_id | id of product |
| stock_pcs | quantity of product |
| price | cost of product |
| shop_id | where the product have sold |
| vip | need credential or not |

### Order

| field | description |
| ------ | ------ |
| *id | uuid of product |
| product_id | id of product |
| qty | number of order |
| price | total bill of the order |
| shop_id | where we have made the order |
| c_id | id of customer  |

**Note:** `c_id` is Customer ID that record who orders the product.

## Decorator Wrapper

### vip credential
members without vip credential  cannot order an item authorized with vip.

```python
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
``` 
### stock quantity 
```python
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
```    

