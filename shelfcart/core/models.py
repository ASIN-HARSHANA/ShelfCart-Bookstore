from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings



STATUS_CHOICE = (
    ("process","processing"),
    ("shipped","Shipped"),
    ("delivered","Delivered"),

)


STATUS = (
    ("draft","Draft"),
    ("disabled","Disabled"),
    ("rejected","Rejected"),
    ("in_review","In Review"),
    ("published","Published"),
)


RATING = (
    (1,"★☆☆☆☆"),
    (2,"★★☆☆☆"),
    (3,"★★★☆☆"),
    (4,"★★★★☆"),
    (5,"★★★★★"),
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="books")
    image = models.ImageField(upload_to="category", default="category.jpg")
    is_active = models.BooleanField(default=True)   


    class Meta:
        verbose_name_plural = "categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))    
    
    def __str__(self):
        return self.title
    
class Tags(models.Model):
    pass    
    
class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Nestify")
    
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg") 
    cover_image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    is_active = models.BooleanField(default=True)
    #description = models.TextField(null=True, blank=True, default="Iam an Amazing Vendor")
    description = RichTextUploadingField(null=True, blank=True, default="Iam an Amazing Vendor")
    
    address = models.CharField(max_length=100, default="123 Main street.")
    contact = models.CharField(max_length=100, default="+123 (456) 789")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100,default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")


    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)   
    #date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
   
    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))    
    
    def __str__(self):
        return self.title
    

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="product")

    title = models.CharField(max_length=100, default="Fresh Pear")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg") 
    author = models.CharField(max_length=100, null=True)
    #description = models.TextField(null=True, blank=True, default="This is the product")
    description = RichTextUploadingField(null=True, blank=True, default="This is the product")

    price = models.DecimalField(max_digits=99999999999,decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=99999999999,decimal_places=2, default="1.99")

    #specifications = models.TextField(null=True, blank=True) 
    specifications = RichTextUploadingField(null=True, blank=True) 

    type = models.CharField(max_length=100, default="Fiction", null=True,blank=True)
    stock_count = models.PositiveIntegerField(default=0)

    tags = TaggableManager(blank=True)
    #tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)



    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe(f'<a href="{self.image.url}" target="_blank"><img src="{self.image.url}" width="50" height="50" /></a>')
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images",default="product.jpg")
    product = models.ForeignKey(Product, related_name= "p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Product Images"
    





############################################ Cart, Order, OrderItems and Address ################################################
############################################ Cart, Order, OrderItems and Address ################################################
############################################ Cart, Order, OrderItems and Address ################################################
############################################ Cart, Order, OrderItems and Address ################################################



class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=99999999999,decimal_places=2, default="1.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")

    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.id}"
    
    class Meta:
        verbose_name_plural = " Cart Order"
 

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=99999999999,decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=99999999999,decimal_places=2, default="1.99")

    class Meta:
        verbose_name_plural = " Cart Order Items" 


    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))               

   

############################################ Product Review, wishlists, Address ################################################
############################################ Product Review, wishlists, Address ################################################
############################################ Product Review, wishlists, Address ################################################
############################################ Product Review, wishlists, Address ################################################


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,related_name="review")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Products Reviews"

    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    


class wishlist_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "wishlists"

    def __str__(self):
        return self.product.title
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=300, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"   



class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.PositiveIntegerField(help_text="Discount percentage")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    


class UsedCoupon(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'coupon')

    def __str__(self):
        return f"{self.user} - {self.coupon.code}"

    