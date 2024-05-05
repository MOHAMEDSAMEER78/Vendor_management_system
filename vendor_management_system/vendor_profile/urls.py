from django.urls import path, include
from .views import Create_vendor, List_vendor, Vendor_detail, Update_vendor, Delete_vendor, Performance_metrics

urlpatterns = [
    path('create/', Create_vendor),
    path('list/',List_vendor),
    path('detail/<int:pk>/', Vendor_detail),
    path('update/<int:pk>/', Update_vendor),
    path('delete/<int:pk>/', Delete_vendor),
    path('performance/<int:pk>/', Performance_metrics),
]

