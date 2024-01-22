# Forex/serializers.py
from rest_framework import serializers
from .models import ForexData

class ForexDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForexData
        fields = ['symbol', 'datetime', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']
