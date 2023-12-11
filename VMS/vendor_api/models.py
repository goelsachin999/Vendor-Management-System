from django.db import models
from django.db.models import Count, Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def update_performance_metrics(self):
        # On-Time Delivery Rate
        completed_pos = self.purchase_orders.filter(status='completed')
        on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now())
        total_completed_pos = completed_pos.count()
        if total_completed_pos > 0:
            self.on_time_delivery_rate = (on_time_deliveries.count() / total_completed_pos) * 100

        # Quality Rating Average
        completed_pos_with_rating = completed_pos.exclude(quality_rating__isnull=True)
        if completed_pos_with_rating.exists():
            self.quality_rating_avg = completed_pos_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg']

        # Average Response Time
        acknowledged_pos = completed_pos.exclude(acknowledgment_date__isnull=True)
        if acknowledged_pos.exists():
            response_times = (acknowledged_pos.values('acknowledgment_date') -
                              acknowledged_pos.values('issue_date'))
            self.average_response_time = response_times.aggregate(Avg('acknowledgment_date'))['acknowledgment_date__avg'].total_seconds()

        # Fulfilment Rate
        successful_fulfillments = completed_pos.filter(issue_date__isnull=False, acknowledgment_date__isnull=False)
        total_completed_pos = completed_pos.count()
        if total_completed_pos > 0:
            self.fulfillment_rate = (successful_fulfillments.count() / total_completed_pos) * 100
        else:
            self.fulfillment_rate = 0

    def save(self, *args, **kwargs):
        self.update_performance_metrics()
        super().save(*args, **kwargs)

class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchase_orders')
    po_number = models.CharField(max_length=20, unique=True)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    @property
    def is_completed(self):
        return self.status == 'completed'

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    if instance.is_completed:
        vendor = instance.vendor
        vendor.on_time_delivery_rate = vendor.purchase_orders.filter(delivery_date__lte=instance.delivery_date, status='completed').count() / vendor.purchase_orders.filter(status='completed').count()
        vendor.quality_rating_avg = vendor.purchase_orders.filter(quality_rating__isnull=False).aggregate(Avg('quality_rating'))['quality_rating__avg']
        vendor.average_response_time = vendor.purchase_orders.filter(acknowledgment_date__isnull=False).aggregate(Avg(models.F('acknowledgment_date') - models.F('issue_date')))['acknowledgment_date__avg']
        vendor.fulfillment_rate = vendor.purchase_orders.filter(status='completed').count() / vendor.purchase_orders.all().count()
        vendor.save()

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

