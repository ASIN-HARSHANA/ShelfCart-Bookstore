from django.contrib import admin
from core.models import Product,Category,Vendor,CartOrder,CartOrderItems,ProductImages,ProductReview,wishlist_model,Address,Coupon


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    extra = 1  # allows at least one image field to appear


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin] 
    list_display = ['user', 'title', 'product_image', 'author', 'price', 'category', 'vendor',  'featured', 'product_status' ,'pid']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']
   
class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image']   

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']  


class CartOrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'qty', 'price', 'total']  


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']

class wishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address', 'status']
    list_display = ['user', 'address', 'status'] 


admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)            
admin.site.register(Vendor,VendorAdmin)            
admin.site.register(CartOrder,CartOrderAdmin)            
admin.site.register(CartOrderItems,CartOrderItemAdmin)  
admin.site.register(ProductReview,ProductReviewAdmin)            
admin.site.register(wishlist_model,wishlistAdmin)     
admin.site.register(Address,AddressAdmin)     
admin.site.register(Coupon)                                   