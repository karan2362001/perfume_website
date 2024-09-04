from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from products.models import Product
from .CustomResponse import CustomResponse
from api.serializers import LoginSerializers,UserSerializers,ProductListSerializer

from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.filters import SearchFilter

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializers
    
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        login(request,user)
        refresh = RefreshToken.for_user(user)
        return CustomResponse(data={'user':UserSerializers(user,context=self.get_serializer()).data,
                         'refresh':str(refresh),
                         'access':str(refresh.access_token)},messages="Data Retrived",status_code=status.HTTP_200_OK)
        # return Response({'user':UserSerializers(user,context=self.get_serializer()).data,
        #                  'refresh':str(refresh),
        #                  'access':str(refresh.access_token)},status=status.HTTP_200_OK)
        
  
        
        
class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({"error": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token to prevent reuse

            return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
        except (TokenError, InvalidToken):
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class ProductApi(generics.ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name','description','price']
    def get(self,request,*args,**kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset,many=True)
            if not serializer.data:
                return CustomResponse(data=[],messages="No Product Found",status_code=status.HTTP_404_NOT_FOUND)
            return CustomResponse(data=serializer.data,messages="Product Retrieved Successfully",status_code=status.HTTP_200_OK)
        except Exception as e:
            return CustomResponse(data=[],messages="An Error Occurred...",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,errors=str(e))
    