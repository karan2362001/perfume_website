from django.shortcuts import render
from products.models import Product
# Create your views here.
def homepage(request):
    
    return render(request,"homepage.html")