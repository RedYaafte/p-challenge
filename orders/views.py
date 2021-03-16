from django.shortcuts import render
from django.utils import timezone

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework_mongoengine import viewsets as v_mongo
from mongoengine.queryset.visitor import Q

from .models import Product, Orders
from .serializers import OrderSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(v_mongo.GenericViewSet):
    serializer_class = OrderSerializer

    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportViewSet(v_mongo.GenericViewSet):
    """
    Format YYYY-MM-DD
    start_date and end_date
    """
    queryset = Orders.objects()

    def list(self, request):
        start_date = self.request.query_params.get('start-date', None)
        end_date = self.request.query_params.get('end-date', None)

        if start_date and end_date:
            qs = Orders.objects(Q(created__gte=start_date)
                                & Q(created__lte=end_date))

            data = []
            p_name = []
            p_list = []
            for p in qs.values_list('products'):
                for i in p:
                    p_list.append(i)
                    if i['name'] not in p_name:
                        p_name.append(i['name'])
                        data.append(
                            {
                                'name': i['name'],
                                'total_qty': 0,
                                'total_price': 0
                            })

            for i in data:
                for p in p_list:
                    if i['name'] == p['name']:
                        price = p['qty'] * p['price']
                        i['total_price'] = sum([price, i['total_price']])
                        i['total_qty'] = sum([p['qty'], i['total_qty']])

            data.sort(key=lambda lt: lt.get('total_price'), reverse=True)
            return Response(data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
