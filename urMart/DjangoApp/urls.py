from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.BackendView.as_view(),name='render_template'),
    path(r'add2order', views.add2order),
    path(r'delFromOrder', views.delFromOrder),
    path(r'findTop3',views.findTop3)

]