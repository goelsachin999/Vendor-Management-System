# vendor_api/urls.py
from django.urls import path
from .views import (
    VendorListCreateView, VendorDetailView,
    PurchaseOrderListCreateView, PurchaseOrderDetailView,
    HistoricalPerformanceListCreateView, HistoricalPerformanceDetailView,
    VendorPerformanceView,AcknowledgePurchaseOrderView
)

urlpatterns = [
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:pk>/', PurchaseOrderDetailView.as_view(), name='purchase-order-detail'),
    path('historical_performances/', HistoricalPerformanceListCreateView.as_view(), name='historical-performance-list-create'),
    path('historical_performances/<int:pk>/', HistoricalPerformanceDetailView.as_view(), name='historical-performance-detail'),    
    path('vendors/<int:pk>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
    path('purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge-purchase-order'),
]
