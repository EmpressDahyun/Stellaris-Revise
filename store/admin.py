from django.contrib import admin
from .models import *
from import_export.admin import ImportExportActionModelAdmin

# Register your models here.

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id','phone_number','barangay','landmark',)
    list_filter = ('barangay', 'phone_number')
    list_per_page = 10
    search_fields = ('barangay', 'landmark')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title", )}

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'product_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'category', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'category', 'short_description')
    prepopulated_fields = {"slug": ("title", )}

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    list_editable = ('quantity',)
    list_filter = ('created_at',)
    list_per_page = 20
    search_fields = ('user', 'product')

class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    list_editable = ('product',)
    list_filter = ('user', 'product')
    list_per_page = 10
    search_fields = ('user', 'product')

class OrderAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    pass
    def phone_number(self,obj):
        return obj.address.phone_number

    def notes(self,obj):
        return obj.address.notes

    list_display = ('id','user','address','phone_number','notes','total_price','status','order_date')
    list_editable = ('status',)
    list_filter = ('id', 'status')
    list_per_page = 10
    search_fields = ('id','status')

class OrderManagementAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    pass
    list_display = ('invoice_no','user','product','quantity','price')
    list_per_page = 10
    list_filter = ('invoice_no',)
    search_fields = ('invoice_no','price')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'event_name', 'event_date', 'event_time', 'event_time_end' , 'status')
    list_editable = ('event_name', 'status')
    list_filter = ('status', 'event_date')
    list_per_page = 20
    search_fields = ('user__username', 'event_name')

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('description', 'image', 'upload_date')
    list_editable = ('image','image')
    list_filter = ('description', 'upload_date')
    list_per_page = 10
    search_fields = ('description', 'description')

class SalesAdmin(admin.ModelAdmin):
    list_display = ('id','total_orders', 'total_products','revenue','subtotal','report_date')
    list_filter = ('report_date',)


admin.site.register(DeliveryInformation, DeliveryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderManagement, OrderManagementAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(ProductReservation)
admin.site.register(Sales, SalesAdmin)
