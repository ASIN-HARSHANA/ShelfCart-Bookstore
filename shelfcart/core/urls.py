from django.urls import path
from core.views import *


app_name="core"

urlpatterns = [

    # Homepage
    path("", index, name="index"),

    #list of products
    path("products/", product_list_view, name="product-list"),

    #details of product
    path("product/<pid>/", product_detail_view, name="product-detail"),


    # Category
    path("category/", category_list_view, name="category-list"),
    path("category/<slug:cid>/", category_product_list_view, name="category-product-list"),


    #vendor
    path("vendors/", vendor_list_view,name="vendor-list"), 
    path("vendor/<vid>/", vendor_detail_view,name="vendor-detail"),   

    #Tags
    path("products/tags/<slug:tag_slug>/", tag_list, name="tags"),
    
    # Add review
    path("ajax-add-review/<int:pid>/", ajax_add_review, name="ajax-add-review"),
    
    # Search
    path("search/", search_view, name="search"),
    
    # filter product
    path("filter-products/", filter_product, name="filter-products"),

    # Add to Cart
    path("add-to-cart/", add_to_cart, name="add-to-cart"),

    # Cart page
    path("cart/", cart_view, name="cart"),
    
    #Delete Item From Cart..
    path("delete-from-cart/", delete_item_from_cart, name="delete_from_cart"), 

    #update cart
    path("update-cart/",update_cart, name="update-cart"),

    #Checkout URL
    path("checkout/",checkout_view, name="checkout"),
  

    path("place-order/", place_order_view, name="place_order"),


    #Dashboard URL
    path("dashboard/",customer_dashboard, name="dashboard"),

    #Order Detail URL
    path("dashboard/order/<int:id>",order_detail, name="order-detail"),

    #making address default
    path('make-default-address/',make_default_address, name='make_default_address'),

    # wishlist page
    path("wishlist/", wishlist_view, name="wishlist"),

    # adding to wishlist 
    path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),

    # Remove from wishlist
    path("remove-from-wishlist/", remove_wishlist, name="remove-from-wishlist"),

    # contact 
    path("contact/", contact, name="contact"),

    path("ajax-contact-form/", ajax_contact_form, name="ajax-contact-form"),


]                                    
