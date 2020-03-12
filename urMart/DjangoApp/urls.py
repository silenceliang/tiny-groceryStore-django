from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.BackendView.as_view(),name='render-template'),
    path(r'add2order', views.add2order, name='add-to-order'),
    path(r'delFromOrder', views.delFromOrder, name='delete-from-order'),
    path(r'findTop3',views.findTop3, name='find-top3')

]