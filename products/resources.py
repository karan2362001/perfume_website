from import_export import resources
from . import models



class CategoryResource(resources.ModelResource):
    class Meta:
        model = models.Category
        
        
class ProductResource(resources.ModelResource):
    class Meta:
        model = models.Product
        
class ProductImageResource(resources.ModelResource):
    class Meta:
        model = models.ProductImage
        
        
