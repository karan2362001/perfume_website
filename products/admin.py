from django.contrib import admin
from . import models
from . import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.
# admin.site.register(models.Category)
# admin.site.register(models.Product)
# admin.site.register(models.ProductImage)


@admin.register(models.Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = resources.CategoryResource
    
    
@admin.register(models.Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = resources.ProductResource
    
    
@admin.register(models.ProductImage)
class ProductImageAdmin(ImportExportModelAdmin):
    resource_class = resources.ProductImageResource