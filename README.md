# DjangoProject

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




