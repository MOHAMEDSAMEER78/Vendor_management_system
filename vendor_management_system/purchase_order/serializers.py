from rest_framework import serializers
from .models import PurchaseOrder

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `PurchaseOrder` instance, given the validated data.
        """
        return PurchaseOrder.objects.create(**validated_data)
