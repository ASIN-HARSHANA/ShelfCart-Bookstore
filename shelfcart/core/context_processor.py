from core.models import Product,Category,Vendor,CartOrder,CartOrderItems,ProductImages,ProductReview,wishlist_model,Address
from django.db.models import Min,Max
from django.contrib import messages

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))

    
    if request.user.is_authenticated:
        wishlist = wishlist_model.objects.filter(user=request.user)
    else:
        wishlist = wishlist_model.objects.none()  

    address = None
    if request.user.is_authenticated:
        address = Address.objects.filter(user=request.user).first()

    return {
        "categories": categories,
        "wishlist": wishlist,
        "address": address,
        "vendors": vendors,
        "min_max_price": min_max_price,
    }
