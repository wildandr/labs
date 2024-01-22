from django.shortcuts import render

# Stock/views.py
from rest_framework import generics
from .models import StockData
from .serializers import StockDataSerializer
from datetime import datetime, timedelta

class StockDataList(generics.ListAPIView):
    serializer_class = StockDataSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned data to the last 24 hours,
        by filtering against a 'datetime' query parameter in the URL.
        """
        queryset = StockData.objects.all()
        last_24_hours = datetime.now() - timedelta(days=1)
        queryset = queryset.filter(datetime__gte=last_24_hours).order_by('datetime')
        return queryset
    
class StockDataDetail(generics.ListAPIView):
    serializer_class = StockDataSerializer

    def get_queryset(self):
        """
        Restricts the returned data to a specific symbol and the last 24 hours.
        """
        symbol = self.kwargs['symbol']
        last_24_hours = datetime.now() - timedelta(days=1)
        return StockData.objects.filter(symbol=symbol, datetime__gte=last_24_hours).order_by('datetime')
