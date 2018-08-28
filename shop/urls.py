from django.urls import path
from . import views

app_name='shop'
urlpatterns = [
    path('',views.allProd_Cat,name='allProd_Cat'),
    path('<slug:c_slug>/',views.allProd_Cat,name='products_by_category'),
    path('<slug:c_slug>/<slug:p_slug>/',views.prod_details,name='prod_details'),

    ]