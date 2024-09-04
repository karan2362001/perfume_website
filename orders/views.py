from django.db import transaction
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart
from api.CustomResponse import CustomResponse

class PlaceOrderView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            shipping_address = request.data.get('shipping_address')
            billing_address = request.data.get('billing_address')

            # Fetch user's cart items
            cart_items = Cart.objects.filter(user=request.user)
            if not cart_items.exists():
                return CustomResponse(messages="Cart is empty", status_code=status.HTTP_400_BAD_REQUEST)

            total_amount = sum(item.product.price * item.quantity for item in cart_items)

            # Start a transaction
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    total_amount=total_amount,
                    shipping_address=shipping_address,
                    billing_address=billing_address,
                )

                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price,
                    )

                # Clear cart after order is placed
                cart_items.delete()

            # Serialize the order for response
            serializer = OrderSerializer(order)
            return CustomResponse(data=serializer.data, messages="Order placed successfully", status_code=status.HTTP_200_OK)

        except Exception as e:
            return CustomResponse(data={}, messages=str(e), status_code=status.HTTP_400_BAD_REQUEST)


class ViewOrderView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class=OrderSerializer
    #queryset = Order.objects.all()
    
    def get(self,request,*args,**kwargs):
        queryset = Order.objects.filter(user=request.user)
        
        print(queryset)
        if not queryset.exists():
            return CustomResponse(data=[], messages="No orders found", status_code=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse(data=serializer.data, messages="Order retrieved ", status_code=status.HTTP_200_OK)