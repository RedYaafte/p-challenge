from rest_framework import serializers
from rest_framework_mongoengine import serializers as m_serializers

from .models import Product, Orders


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductsSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    price = serializers.FloatField(required=True)
    qty = serializers.IntegerField(required=True)


class OrderSerializer(m_serializers.DynamicDocumentSerializer):
    products = ProductsSerializer(many=True)

    class Meta:
        model = Orders
        fields = ['id', 'client', 'products', 'total_price', 'user_email']

    def create(seld, validated_data):
        client = validated_data.get('client')
        products = validated_data.get('products')
        total_price = validated_data.get('total_price', 0)
        user_email = validated_data.get('user_email', None)

        if not total_price:
            for p in products:
                total_price = (p['qty'] * p['price']) + total_price

        order = Orders.objects.create(
            client=client,
            products=products,
            total_price=total_price,
            user_email=user_email
        )

        for product in products:
            p_name = product.get('name')
            if Product.objects.filter(name=p_name).exists():
                pass
            else:
                Product.objects.create(name=p_name, price=product.get('price'))
        return order
