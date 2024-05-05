from rest_framework.response import Response
from rest_framework import status
from .models import Vendor
from .serializers import VendorSerializer
from rest_framework.decorators import api_view

@api_view(['POST'])
def Create_vendor(request):
    serializer = VendorSerializer(data=request.data)
    if serializer.is_valid():
        vendor = serializer.save()
        return Response({'status': 'success', 'vendor_id': vendor.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def List_vendor(request):
    vendors = Vendor.objects.all()
    serializer = VendorSerializer(vendors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def Vendor_detail(request, pk):
    try:
        vendor = Vendor.objects.get(pk=pk)
    except Vendor.DoesNotExist:
        return Response({'status': 'error', 'message': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = VendorSerializer(vendor)
    return Response(serializer.data)

@api_view(['PUT'])
def Update_vendor(request, pk):
    try:
        vendor = Vendor.objects.get(pk=pk)
    except Vendor.DoesNotExist:
        return Response({'status': 'error', 'message': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = VendorSerializer(vendor, data=request.data, partial=True)
    if serializer.is_valid():
        vendor = serializer.save()
        return Response({'status': 'success', 'vendor_id': vendor.id}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def Delete_vendor(request, pk):
    try:
        vendor = Vendor.objects.get(pk=pk)
    except Vendor.DoesNotExist:
        return Response({'status': 'error', 'message': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
    vendor.delete()
    return Response({'status': 'success', 'message': 'Vendor deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def Performance_metrics(request, pk):
    try:
        vendor = Vendor.objects.get(pk=pk)
    except Vendor.DoesNotExist:
        return Response({'status': 'error', 'message': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Calculate performance metrics
    on_time_delivery_rate = vendor.calculate_on_time_delivery_rate()
    quality_rating_avg = vendor.calculate_quality_rating_avg()
    average_response_time = vendor.calculate_average_response_time()
    fulfilment_rate = vendor.calculate_fulfilment_rate()

    performance_metrics = {
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'average_response_time': average_response_time,
        'fulfilment_rate': fulfilment_rate
    }

    request.data['on_time_delivery_rate'] = on_time_delivery_rate
    request.data['quality_rating_avg'] = quality_rating_avg
    request.data['average_response_time'] = average_response_time
    request.data['fulfilment_rate'] = fulfilment_rate
    
    serializer = VendorSerializer(vendor, data=request.data, partial=True)
    if serializer.is_valid():
        vendor = serializer.save()
        return Response(performance_metrics)

    return Response(performance_metrics)