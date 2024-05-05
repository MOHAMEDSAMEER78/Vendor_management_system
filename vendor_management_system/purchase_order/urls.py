from django.urls import path
from .views import Create_purchase_order, List_purchase_order, Purchase_order_detail, Update_purchase_order, Delete_purchase_order

urlpatterns = [
    path('create/', Create_purchase_order), 
    path('list/', List_purchase_order),
    path('detail/<int:pk>/', Purchase_order_detail),
    path('update/<int:pk>/', Update_purchase_order),
    path('delete/<int:pk>/', Delete_purchase_order),
]
