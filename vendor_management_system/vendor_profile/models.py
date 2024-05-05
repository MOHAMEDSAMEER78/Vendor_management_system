from django.db import models
from django.db.models import Avg, ExpressionWrapper, F, DateTimeField
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    vendor_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def calculate_on_time_delivery_rate(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')
        total_completed_orders = completed_orders.count()
        if total_completed_orders == 0:
            return 0
        on_time_orders = completed_orders.filter(delivery_date__lte=timezone.now())
        on_time_delivery_rate = (on_time_orders.count() / total_completed_orders) * 100
        return round(on_time_delivery_rate, 2)

    def calculate_quality_rating_avg(self):
        completed_orders = self.purchaseorder_set.filter(status='completed').exclude(quality_rating__isnull=True)
        if completed_orders.count() == 0:
            return None
        quality_rating_avg = completed_orders.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']
        return round(quality_rating_avg, 2)

    def calculate_average_response_time(self):
        completed_orders = self.purchaseorder_set.filter(status='completed').exclude(acknowledgment_date__isnull=True)
        if completed_orders.count() == 0:
            return None
        total_response_time = timedelta()
        for order in completed_orders:
            total_response_time += order.acknowledgment_date - order.issue_date
        avg_response_time = total_response_time / completed_orders.count()
        avg_response_time_minutes = avg_response_time.total_seconds() / 60
        return round(avg_response_time_minutes, 2)

    def calculate_fulfilment_rate(self):
        all_orders = self.purchaseorder_set.all()
        if all_orders.count() == 0:
            return 0
        fulfilled_orders = all_orders.filter(status='completed')
        fulfilment_rate = (fulfilled_orders.count() / all_orders.count()) * 100
        return round(fulfilment_rate, 2)



class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()