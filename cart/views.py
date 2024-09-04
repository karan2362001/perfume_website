from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.models import User
from products.models import Product
from .models import Cart
from api.CustomResponse import CustomResponse
from datetime import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
 
# Create your views here.
from .serializers import CartSerializer
class CartItems(generics.CreateAPIView):
    serializer_class=CartSerializer
    queryset = Cart.objects.all()
    permission_classes=[IsAuthenticated]
    authentication_classes= [JWTAuthentication]
    
    def get(self,request,*args,**kwargs):
        queryset= Cart.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset,many=True)
        # if serializer.is_valid(raise_exception=True):
        return CustomResponse(data=serializer.data,messages="Cart items retrieved successfully",status_code=status.HTTP_200_OK)
        
        
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            product_id=request.query_params.get("product_id")
            product=Product.objects.filter(id=product_id).first()
            print(product_id)
            serializer.validated_data['user']=request.user
            serializer.validated_data['product']=product
            
            serializer.save()
            return CustomResponse(data=serializer.data,messages="Data store successfully",status_code=status.HTTP_200_OK)

    
    def delete(self,request,*args,**kwargs):
        cart_id=request.query_params.get("cart_id")
        queryset=Cart.objects.filter(user=request.user,id=cart_id).first()
        # serializer=self.get_serializer(queryset,many=True)  
        if queryset:
            queryset.delete()
            return CustomResponse(data=[],messages="Item removed from cart successfully", status_code=status.HTTP_204_NO_CONTENT)
        
        return CustomResponse(messages="Item not found in cart", status_code=status.HTTP_404_NOT_FOUND)
             
    
    def patch(self,request,*args,**kwargs):
        cart_id=request.query_params.get("cart_id")
        action = request.query_params.get("action")
        queryset=Cart.objects.filter(user=request.user,id=cart_id).first()
        if not queryset:
            return CustomResponse(messages="Item not found in cart", status_code=status.HTTP_404_NOT_FOUND)
        
        if action=="increment":
            queryset.quantity+=1
            queryset.save()
            return CustomResponse(data={"quantity": queryset.quantity}, messages="Quantity increased", status_code=status.HTTP_200_OK)
        elif action=="decrement":
            if queryset.quantity>1:
                queryset.quantity-=1
                queryset.save()
                return CustomResponse(data={"quantity": queryset.quantity}, messages="Quantity decreased", status_code=status.HTTP_200_OK)
            else:
                return CustomResponse(messages="Cannot decrement quantity below 1", status_code=status.HTTP_400_BAD_REQUEST)
       
            
        