from django.shortcuts import render

# Create your views here.
from .serializers import ReviewSerializer
from api.CustomResponse import CustomResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from .models import Review
from products.models import Product
from rest_framework.filters import OrderingFilter,SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

class ReviewView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    serializer_class=ReviewSerializer
    filter_backends=[OrderingFilter,DjangoFilterBackend,SearchFilter]
    filterset_fields=['product', 'user']
    search_fields=['rating','comment']
    queryset = Review.objects.all()
    ordering_fields = ['rating', 'created_at', 'updated_at']  # Example fields for ordering
    ordering = ['-created_at']
    
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        product_id = request.query_params.get('product_id')
        product = Product.objects.filter(id=product_id).first()
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(product=product,user=request.user)
            return CustomResponse(data=serializer.data,messages="Review added successfully",status_code=status.HTTP_201_CREATED)
        else:
            return CustomResponse(data=serializer.errors, messages="Invalid data provided.", status_code=status.HTTP_400_BAD_REQUEST)


    def get(self,request,*args,**kwargs):
        #product_id = request.query_params.get('product_id')
        reviews = self.filter_queryset(self.get_queryset())
        serializer=self.get_serializer(reviews,many=True)
        
        return CustomResponse(data=serializer.data,messages="Review for the Product",status_code=status.HTTP_200_OK)
    
    def delete(self,request,*args,**kwargs):
        review_id = request.query_params.get('review_id')
        review=Review.objects.get(id=review_id)
        review.delete()
        return CustomResponse(data={"message": "Review deleted successfully"}, status_code=status.HTTP_200_OK)