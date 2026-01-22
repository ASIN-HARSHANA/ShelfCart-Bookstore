from django.shortcuts import render, redirect, get_object_or_404
from userauths.models import User
from core.forms import VendorForm
from core.models import Product,Category,Vendor
from django.contrib import messages




# Create your views here.

def dashboard(request):
    return render(request, 'adminpanel/dashboard.html')


def users_list(request):
    users = User.objects.all().order_by('-id')
    return render(request, 'adminpanel/users.html', {'users': users})

def products_list(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'adminpanel/products.html', {'products': products})


def categories(request):
    categories = Category.objects.filter(is_active=True).order_by('-id')
    return render(request, 'adminpanel/categories.html', {'categories': categories})


def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        messages.success(request, 'Category added successfully')
        return redirect('adminpanel:categories')

    return render(request, 'adminpanel/category_add.html')


def category_edit(request, id):   
    category = get_object_or_404(Category, id=id)

    if request.method == 'POST':
        category.title = request.POST.get('name')
        category.save()
        messages.success(request, 'Category updated successfully')
        return redirect('adminpanel:categories')

    return render(request, 'adminpanel/category_edit.html', {
        'category': category
    })



def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    category.is_active = False   
    category.save()
    messages.success(request, 'Category deleted')
    return redirect('adminpanel:categories')


def vendors(request):
    vendors = Vendor.objects.all().order_by("-id")
    return render(request, "adminpanel/vendors.html", {"vendors": vendors})





def vendor_add(request):
    if request.method == "POST":
        form = VendorForm(request.POST, request.FILES)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.is_active = True
            vendor.save()
            messages.success(request, "Vendor added successfully")
            return redirect("adminpanel:vendors")
    else:
        form = VendorForm()

    return render(request, "adminpanel/vendor_add.html", {"form": form})



def vendor_edit(request, id):
    vendor = Vendor.objects.get(id=id)
    form = VendorForm(instance=vendor)

    if request.method == "POST":
        form = VendorForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect("adminpanel:vendors")

    return render(request, "adminpanel/vendor_edit.html", {"form": form,"vendor": vendor})


def vendor_delete(request, id):
    vendor = get_object_or_404(Vendor, id=id)
    vendor.is_active = False   # soft delete
    vendor.save()
    messages.success(request, 'Vendor deleted')
    return redirect('adminpanel:vendors')