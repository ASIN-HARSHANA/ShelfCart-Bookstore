from django.shortcuts import render , get_object_or_404,redirect
from django.http import JsonResponse
from django.db.models import Count,Avg
from taggit.models import Tag
from core.models import *
from core.forms import *
from userauths.models import ContactUs,Profile
from django.template.loader import render_to_string
from django.contrib import messages
from decimal import Decimal, InvalidOperation
import re
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.urls import reverse


def index(request):
    # products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published" , featured=True)


    context={
        "products": products
    }
    return render(request,'core/index.html',context)

def product_list_view(request):
    products = Product.objects.filter(product_status="published")

    context={
        "products": products
    }
    return render(request,'core/product-list.html',context)

def category_list_view(request):
    # categories = Category.objects.all()
    categories = Category.objects.all().annotate(product_count=Count("products"))

    context = {
        "categories":categories
    }
    return render(request, 'core/category-list.html',context)
       

def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)

    context ={
        "category":category,
        "products":products,
    }
    return render(request,"core/category-product-list.html",context)


def vendor_list_view(request):
    vendors =Vendor.objects.all()
    context = {
        "vendors":vendors,
    }
    return render(request,"core/vendor-list.html",context)


def vendor_detail_view(request, vid):
    vendor =Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status="published")

    context = {
        "vendor":vendor,
        "products":products,

    }
    return render(request,"core/vendor-detail.html",context)





def product_detail_view(request, pid):
    try:
        product = Product.objects.get(pid=pid, status=True)
    except Product.DoesNotExist:
        messages.warning(request, "This product is currently unavailable or blocked.")
        return redirect('core:product-list')

    try:
        stock = int(product.stock_count)
    except:
        stock = 0

    is_out_of_stock = (not product.in_stock) or (stock <= 0)

    related_products = Product.objects.filter( category=product.category, status=True).exclude(pid=pid)[:8]

    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    average_rating = reviews.aggregate(rating=Avg('rating'))

    review_form = ProductReviewForm()
    make_review = True

    if request.user.is_authenticated:
        if ProductReview.objects.filter(user=request.user, product=product).exists():
            make_review = False

    p_image = product.p_images.all()

    context = {
        "p": product,
        "p_image": p_image,
        "reviews": reviews,
        "average_rating": average_rating,
        "review_form": review_form,
        "make_review": make_review,
        "related_products": related_products,
        "is_out_of_stock": is_out_of_stock,
        "stock": stock,
    }

    return render(request, "core/product-detail.html", context)





def tag_list(request,tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by("-id")

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        "products": products,
        "tag": tag

    }    

    return render(request, "core/tag.html", context)


def ajax_add_review(request,pid):
    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating'],

    )
    
    context = {
        'user' : user.username,
        'review' : request.POST['review'],
        'rating' : request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'average_reviews': average_reviews
        }
    )


def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query).order_by("-date")

    context = {
       "products": products,
       "query": query,
    }
    return render(request, "core/search.html",context)


def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.filter(product_status="published").order_by("-id").distinct()

    products =products.filter(price__gte=min_price)
    products =products.filter(price__lte=max_price)

    if len(categories) >0:
        products = products.filter(category__id__in=categories).distinct()
    if len(vendors) >0:
        products = products.filter(vendor__id__in=vendors).distinct()
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    data = render_to_string('core/async/product-list.html', {'products': products})
    return JsonResponse({'data': data})


def add_to_cart(request):
    product_id = request.GET.get('id')
    qty = int(request.GET.get('qty', 1))

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

    cart_data = request.session.get('cart_data_obj', {})

    existing_qty = int(cart_data.get(str(product.id), {}).get('qty', 0))
    available_stock = product.stock_count - existing_qty

    if qty > available_stock:
        return JsonResponse({
            "error": f"Only {available_stock} items available"
        }, status=400)

    if str(product.id) in cart_data:
        cart_data[str(product.id)]['qty'] = existing_qty + qty
    else:
        cart_data[str(product.id)] = {
            'title': product.title,
            'qty': qty,
            'price': str(product.price),
            'image': product.image.url,
            'pid': product.pid,
        }

    request.session['cart_data_obj'] = cart_data

    return JsonResponse({
        "data": cart_data,
        "totalcartitems": len(cart_data)
    })




def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            try:
                price = float(item.get('price', 0) or 0)
                qty = int(item.get('qty', 1) or 1)
            except ValueError:
                price = 0
                qty = 1
            cart_total_amount += qty * price

        return render(request, "core/cart.html", {'cart_data': request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request, "Your Cart is Empty")
        return redirect("core:index")
          



def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
       if product_id in request.session['cart_data_obj']:
        cart_data = request.session['cart_data_obj']
        del request.session['cart_data_obj'][product_id]
        request.session['cart_data_obj'] =cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            try:
                price = float(item.get('price', 0) or 0)
                qty = int(item.get('qty', 1) or 1)
            except ValueError:
                price = 0
                qty = 1
            cart_total_amount += qty * price

    context = render_to_string('core/async/cart-list.html', {'cart_data': request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})  
            


def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    
    if 'cart_data_obj' in request.session:
       if product_id in request.session['cart_data_obj']:
        cart_data = request.session['cart_data_obj']
        cart_data[str(request.GET['id'])]['qty'] = product_qty
        request.session['cart_data_obj'] =cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            try:
                price = float(item.get('price', 0) or 0)
                qty = int(item.get('qty', 1) or 1)
            except ValueError:
                price = 0
                qty = 1
            cart_total_amount += qty * price

    context = render_to_string('core/async/cart-list.html', {'cart_data': request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})  
    
            


def checkout_view(request):
    cart = request.session.get('cart_data_obj', {})
    cart_total_amount = 0

    for item in cart.values():
        cart_total_amount += float(item['price']) * int(item['qty'])

    discount_amount = 0
    final_amount = cart_total_amount
    coupon_code = None

    if request.method == "POST":
        code = request.POST.get("coupon")
        coupon = Coupon.objects.filter(code=code, active=True).first()

        if not coupon:
            messages.error(request, "Invalid coupon")
        elif UsedCoupon.objects.filter(user=request.user, coupon=coupon).exists():
            messages.error(request, "Coupon already used")
        else:
            discount_amount = (coupon.discount / 100) * cart_total_amount
            request.session['coupon'] = {
                "code": coupon.code,
                "discount_amount": float(discount_amount),
                "coupon_id": coupon.id
            }
            messages.success(request, "Coupon applied Successfully")

    coupon_data = request.session.get("coupon")
    if coupon_data:
        discount_amount = coupon_data.get('discount_amount', 0)
        coupon_code = coupon_data["code"]
    final_amount = cart_total_amount - discount_amount

    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except:
        messages.warning(request, "There are multiple addresses, only one should be activated.")   
        active_address = None

    context = {"cart_data": cart,"cart_total_amount": cart_total_amount,  "discount_amount": discount_amount, "final_amount": final_amount, "coupon_code": coupon_code,'totalcartitems': len(request.session['cart_data_obj']),"active_address" : active_address}

    return render(request, "core/checkout.html", context)




@login_required
def place_order_view(request):
    cart = request.session.get("cart_data_obj")

    if not cart:
        messages.error(request, "Cart empty")
        return redirect("core:cart")

    subtotal = 0
    for item in cart.values():
        subtotal += float(item['price']) * int(item['qty'])

    coupon_data = request.session.get("coupon")
    discount = 0
    coupon_code = None

    if coupon_data:
        discount = coupon_data.get('discount_amount', 0)
        coupon_code = coupon_data["code"]

    final_price = subtotal - discount

    order = CartOrder.objects.create(
        user=request.user,
        price=final_price,
        coupon_code=coupon_code,
        discount_amount=discount
    )

    for item in cart.values():
        product = Product.objects.get(pid=item["pid"])
        qty = int(item["qty"])

        if product.stock_count < qty:
            messages.error(
                request,
                f"Insufficient stock for {product.title}"
            )
            return redirect("core:cart")

        product.stock_count -= qty

        if product.stock_count <= 0:
            product.stock_count = 0
            product.in_stock = False

        product.save()

        CartOrderItems.objects.create(
            order=order,
            item=item["title"],
            image=item["image"],
            qty=qty,
            price=item["price"],
            total=float(item["price"]) * qty
        )

    if coupon_data:
        UsedCoupon.objects.create(
            user=request.user,
            coupon_id=coupon_data["coupon_id"]
        )

    del request.session["cart_data_obj"]
    request.session.pop("coupon", None)

    messages.success(request, "Order placed successfully")

    url = reverse('core:order-detail', args=[order.id])
    return redirect(f"{url}?new=1")




@login_required
def customer_dashboard(request):
    orders = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)



    if request.method == "POST":
        address = request.POST.get("address")
        contact = request.POST.get("contact") 

        new_address = Address.objects.create(
            user = request.user,
            address = address,
            contact = contact,
        )
        messages.success(request, "Address Added Successfully...")
        return redirect("core:dashboard") 

    user_profile, created = Profile.objects.get_or_create(user=request.user)

    context = {
        "user_profile": user_profile,
        "orders": orders,
        "address": address,
    }
    return render(request, 'core/dashboard.html',context)

def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderItems.objects.filter(order=order)

    context = {
        "order_items": order_items
    }
    return render(request, 'core/order-detail.html',context)

@login_required
def make_default_address(request):
    address_id = request.GET.get('id')
    if address_id:
        # Reset all to False
        Address.objects.filter(user=request.user).update(status=False)
        # Set selected to True
        Address.objects.filter(id=address_id, user=request.user).update(status=True)
        return JsonResponse({'boolean': True})
    
    return JsonResponse({'boolean': False})

@login_required
def wishlist_view(request):
    wishlist = wishlist_model.objects.filter(user=request.user)
    context = {
        "W": wishlist,
    }
    return render(request, "core/wishlist.html", context)


def add_to_wishlist(request):
    product_id = request.GET.get('id')
    product = Product.objects.get(id=product_id)

    wishlist_item = wishlist_model.objects.filter(product=product,user=request.user)

    if wishlist_item.exists():
        status = "exists"
    else:
        wishlist_model.objects.create(product=product,user=request.user)
        status = "added"

    wishlist_count = wishlist_model.objects.filter(user=request.user).count()

    return JsonResponse({
        "bool": True,
        "status": status,
        "wishlist_count": wishlist_count,
    })





def remove_wishlist(request):
    pid = request.GET.get("id")

    wishlist_model.objects.filter(id=pid, user=request.user).delete()

    wishlist = wishlist_model.objects.filter(user=request.user)
    wishlist_count = wishlist.count()

    context = {
        "W": wishlist
    }

    html = render_to_string(
        "core/async/wishlist-list.html",
        context,
        request=request
    )

    return JsonResponse({
        "data": html,
        "wishlist_count": wishlist_count
    })


def contact(request):
    return render(request, "core/contact.html")

def ajax_contact_form(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        full_name = full_name,
        email = email,
        phone =  phone,
        subject = subject,
        message = message,

    )

    data = {
        "bool": True,
        "message": "Message Sent Successfully"
    }
    return JsonResponse({"data":data})