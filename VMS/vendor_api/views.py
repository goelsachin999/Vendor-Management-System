from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer,VendorPerformanceSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class HistoricalPerformanceListCreateView(generics.ListCreateAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer

class HistoricalPerformanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer

class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    lookup_field = 'pk'

class AcknowledgePurchaseOrderView(APIView):
    def post(self, request, pk):
        purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        return Response(status=status.HTTP_200_OK)
