from rest_framework import serializers
from .models import Order, OrderItem, Bill



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields="__all__"
        
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'order_date', 'total_amount', 'status', 'shipping_address', 
                  'billing_address', 'payment_status', 'transaction_id', 'created_at', 
                  'updated_at', 'order_items']