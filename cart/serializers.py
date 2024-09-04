from rest_framework import serializers
from .models import Cart



class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = ['user', 'product']
        
        
    def to_representation(self, instance):
        representation=super().to_representation(instance)
        representation['added_date'] = instance.added_date.strftime('%B %d, %Y %I:%M %p')
        representation['created_at'] = instance.created_at.strftime('%B %d, %Y %I:%M %p')
        representation['updated_at'] = instance.updated_at.strftime('%B %d, %Y %I:%M %p')
        representation['quantity']=f"{instance.quantity} times "
        representation
        return representation