from rest_framework.response import Response
from rest_framework import status
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from rest_framework.decorators import api_view

@api_view(['POST'])
def Create_purchase_order(request):
    serializer = PurchaseOrderSerializer(data=request.data)
    if serializer.is_valid():
        purchase_order = serializer.save()
        return Response({'status': 'success', 'purchase_order_id': purchase_order.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def List_purchase_order(request):
    purchase_orders = PurchaseOrder.objects.all()
    serializer = PurchaseOrderSerializer(purchase_orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def Purchase_order_detail(request, pk):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=pk)
    except PurchaseOrder.DoesNotExist:
        return Response({'status': 'error', 'message': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PurchaseOrderSerializer(purchase_order)
    return Response(serializer.data)

@api_view(['PUT'])
def Update_purchase_order(request, pk):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=pk)
    except PurchaseOrder.DoesNotExist:
        return Response({'status': 'error', 'message': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PurchaseOrderSerializer(purchase_order, data=request.data, partial=True)
    if serializer.is_valid():
        purchase_order = serializer.save()
        return Response({'status': 'success', 'purchase_order_id': purchase_order.id}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def Delete_purchase_order(request, pk):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=pk)
    except PurchaseOrder.DoesNotExist:
        return Response({'status': 'error', 'message': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)
    purchase_order.delete()
    return Response({'status': 'success', 'message': 'Purchase Order deleted'}, status=status.HTTP_204_NO_CONTENT)
