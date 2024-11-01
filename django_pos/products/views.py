from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, Store, StoreInventory, Vendor, Purchase, SalesReport, PurchaseReport, AbsenceReport
import datetime
from authentication.models import Employee
from sales.models import Sale

def CategoriesListView(request):
    if request.user.is_admin:
        # Admins see all categories created by their employees
        categories = Category.objects.filter(user__in=request.user.employees.all())
    else:
        # Regular users see only their own categories
        categories = Category.objects.filter(user=request.user)

    context = {
        "active_icon": "products_categories",
        "categories": categories.order_by('-date_added')
    }
    return render(request, "products/categories.html", context=context)

@login_required(login_url="/accounts/login/")
def CategoriesAddView(request):
    context = {
        "active_icon": "products_categories",
        "category_status": Category.STATUS_CHOICES  # Correctly reference status choices
    }

    if request.method == 'POST':
        data = request.POST
        attributes = {
            "user": request.user,  # Set the logged-in user
            "name": data.get('name'),  # Use .get() to avoid KeyError
            "description": data.get('description'),
            "status": data.get('state')  # Ensure 'state' is the correct key for status
        }

        # Check if a category with the same attributes exists
        if Category.objects.filter(user=request.user, name=attributes['name']).exists():
            messages.error(request, 'Category already exists!', extra_tags="warning")
            return redirect('products:categories_add')

        try:
            new_category = Category.objects.create(**attributes)
            messages.success(request, f'Category: {attributes["name"]} created successfully!', extra_tags="success")
            return redirect('products:categories_list')
        except Exception as e:
            messages.error(request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('products:categories_add')

    return render(request, "products/categories_add.html", context=context)


@login_required(login_url="/accounts/login/")
def CategoriesUpdateView(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)

    context = {
        "active_icon": "products_categories",
        "category_status": Category.status.field.choices,
        "category": category
    }

    if request.method == 'POST':
        data = request.POST
        attributes = {
            "name": data['name'],
            "status": data['state'],
            "description": data['description']
        }

        if Category.objects.filter(user=request.user, **attributes).exclude(id=category_id).exists():
            messages.error(request, 'Category already exists!', extra_tags="warning")
            return redirect('products:categories_update', category_id=category_id)

        # Update the category
        for attr, value in attributes.items():
            setattr(category, attr, value)
        category.save()

        messages.success(request, f'Category: {category.name} updated successfully!', extra_tags="success")
        return redirect('products:categories_list')

    return render(request, "products/categories_update.html", context=context)

@login_required(login_url="/accounts/login/")
def CategoriesDeleteView(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    category.delete()
    messages.success(request, f'Category: {category.name} deleted!', extra_tags="success")
    return redirect('products:categories_list')

@login_required(login_url="/accounts/login/")
def ProductsListView(request):
    if request.user.is_admin:
        # Admins see all products created by their employees
        products = Product.objects.filter(user__in=request.user.employees.all())
    else:
        # Regular users see only their own products
        products = Product.objects.filter(user=request.user)

    context = {
        "active_icon": "products",
        "products": products.order_by('-date_added')
    }
    return render(request, "products/products.html", context=context)


@login_required(login_url="/accounts/login/")
def ProductsAddView(request):
    context = {
        "active_icon": "products_categories",
        "product_status": Product.status.field.choices,
        "categories": request.user.categories.filter(status="ACTIVE")
    }

    if request.method == 'POST':
        data = request.POST
        attributes = {
            "user": request.user,  # Set the logged-in user
            "name": data.get('name'),  # Use .get() to avoid KeyError
            "status": data.get('state'),
            "description": data.get('description'),
            "category": get_object_or_404(Category, id=data.get('category'), user=request.user),  # Ensure category belongs to the user
            "price": data.get('price'),
            "capacity": data.get('capacity')
        }

        # Check if a product with the same name and user exists
        if Product.objects.filter(user=request.user, name=attributes["name"]).exists():
            messages.error(request, 'Product already exists!', extra_tags="warning")
            return redirect('products:products_add')

        try:
            new_product = Product.objects.create(**attributes)
            messages.success(request, f'Product: {attributes["name"]} created successfully!', extra_tags="success")
            return redirect('products:products_list')
        except Exception as e:
            messages.error(request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('products:products_add')

    return render(request, "products/products_add.html", context=context)


@login_required(login_url="/accounts/login/")
def ProductsUpdateView(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)

    context = {
        "active_icon": "products",
        "product_status": Product.status.field.choices,
        "product": product,
        "categories": request.user.categories.all()
    }

    if request.method == 'POST':
        data = request.POST
        attributes = {
            "name": data['name'],
            "status": data['state'],
            "description": data['description'],
            "category": get_object_or_404(Category, id=data['category'], user=request.user),
            "price": data['price']
        }

        if Product.objects.filter(user=request.user, **attributes).exclude(id=product_id).exists():
            messages.error(request, 'Product already exists!', extra_tags="warning")
            return redirect('products:products_update', product_id=product_id)

        for attr, value in attributes.items():
            setattr(product, attr, value)
        product.save()

        messages.success(request, f'Product: {product.name} updated successfully!', extra_tags="success")
        return redirect('products:products_list')

    return render(request, "products/products_update.html", context=context)

@login_required(login_url="/accounts/login/")
def ProductsDeleteView(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)
    product.delete()
    messages.success(request, f'Product: {product.name} deleted!', extra_tags="success")
    return redirect('products:products_list')

# Similar views can be created for Store, Vendor, and Purchase models with the same permission checks.



def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url="/accounts/login/")
def GetProductsAJAXView(request):
    if request.method == 'POST':
        if is_ajax(request=request):
            data = []

            products = Product.objects.filter(
                name__icontains=request.POST['term'])
            for product in products[0:10]:
                item = product.to_json()
                data.append(item)

            return JsonResponse(data, safe=False)

from .models import Purchase, Store, Vendor
from .forms import PurchaseForm, VendorForm, StoreForm

@login_required(login_url="/accounts/login/")
def purchase_list(request):
    purchases = Purchase.objects.all().order_by('-date_added')
    return render(request, 'products/purchase_list.html', {'purchases': purchases})

@login_required(login_url="/accounts/login/")
def vendors_list(request):
    vendors = Vendor.objects.all().order_by('-date_added')
    return render(request, 'customers/vendors_list.html', {'vendors': vendors})

@login_required(login_url="/accounts/login/")
def add_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:purchase_list')  # Make sure the redirect name matches the URL name
    else:
        form = PurchaseForm()
    return render(request, 'products/add_purchase.html', {'form': form, 'stores': Store.objects.all(), 'products': Product.objects.all(), 'vendors': Vendor.objects.all()})

@login_required(login_url="/accounts/login/")
def add_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:store_list')  # Adjust redirect URL as needed
    else:
        form = StoreForm()
    return render(request, 'products/add_store.html', {'form': form})

@login_required(login_url="/accounts/login/")
def store_list(request):
    stores = Store.objects.all().order_by('-date_added')  # Query for Store objects
    return render(request, 'products/store_list.html', {'stores': stores}) 

def store_inventory_view(request, store_id):
    # Get the store object based on store_id
    store = get_object_or_404(Store, pk=store_id)
    
    # Get inventory items for the store
    inventory_items = StoreInventory.objects.filter(store=store)
    
    context = {
        'store': store,
        'inventory_items': inventory_items,
    }
    return render(request, 'products/store_inventory.html', context)

@login_required(login_url="/accounts/login/")
def add_store(request):
    """Add a new store."""
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)  # Don't save just yet
            store.user = request.user  # Set the user
            store.save()  # Now save
            return redirect('products:store_list')  # Adjust redirect URL as needed
    else:
        form = StoreForm()
    return render(request, 'products/add_store.html', {'form': form})

@login_required(login_url="/accounts/login/")
def store_list(request):
    """List all stores added by the logged-in user or their employees if the user is an admin."""
    
    if request.user.is_admin:
        # Admins see all stores added by their employees
        stores = Store.objects.filter(user__in=request.user.employees.all()).order_by('-date_added')
    else:
        # Regular users see only their own stores
        stores = Store.objects.filter(user=request.user).order_by('-date_added')

    return render(request, 'products/store_list.html', {'stores': stores})

@login_required(login_url="/accounts/login/")
def store_inventory_view(request, store_id):
    """View inventory for a specific store."""
    store = get_object_or_404(Store, pk=store_id, user=request.user)  # Ensure the store belongs to the user
    inventory_items = StoreInventory.objects.filter(store=store)
    
    context = {
        'store': store,
        'inventory_items': inventory_items,
    }
    return render(request, 'products/store_inventory.html', context)

@login_required(login_url="/accounts/login/")
def add_vendor(request):
    """Add a new vendor."""
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)  # Don't save just yet
            vendor.user = request.user  # Set the user
            vendor.save()  # Now save
            return redirect('products:vendors_list')  # Adjust redirect URL as needed
    else:
        form = VendorForm()
    return render(request, 'products/add_vendor.html', {'form': form})

@login_required(login_url="/accounts/login/")
def vendor_list(request):
    """List all vendors added by the logged-in user."""
    # Filter vendors by the logged-in user
    vendors = Vendor.objects.filter(user=request.user).order_by('-date_added')
    
    # Render the template with the vendors list
    return render(request, 'products/vendor_list.html', {'vendors': vendors})

@login_required(login_url="/accounts/login/")
def daily_sales_report(request):
    """Generate daily sales report for the logged-in user's store."""
    today = datetime.date.today()

    # Getting the sales based on the user role
    if request.user.is_admin or request.user.is_superuser:
        # Get all employees managed by this admin user
        employee_queryset = Employee.objects.filter(admin=request.user)
        # Get sales for all managed employees
        reports = Sale.objects.filter(employee__in=employee_queryset.values_list('employee', flat=True), date_added__date=today)
    else:
        # For regular employees, filter based on the logged-in employee
        employee_queryset = Employee.objects.filter(employee=request.user)
        reports = Sale.objects.filter(employee__in=employee_queryset.values_list('employee', flat=True), date_added__date=today)

    # Calculate total sales amount for today's reports
    total_sales = reports.aggregate(total=Sum('grand_total'))['total'] or 0

    return render(request, 'products/daily_sales_report.html', {
        'reports': reports,
        'total_sales': total_sales,
    })

@login_required(login_url="/accounts/login/")
def daily_purchase_report(request):
    """Generate daily purchase report for the logged-in user's store."""
    today = datetime.date.today()  # Get today's date

    if request.user.is_admin or request.user.is_superuser:
        employee_queryset = Employee.objects.filter(admin=request.user)  # Get employees managed by the admin
        # Correct the filtering to ensure it retrieves CustomUser instances
        reports = PurchaseReport.objects.filter(employee__in=employee_queryset.values_list('employee', flat=True), date=today)
    else:
        # For regular employees, filter based on the logged-in employee
        employee_queryset = Employee.objects.filter(employee=request.user)  # Get the logged-in employee instance
        reports = PurchaseReport.objects.filter(employee__in=employee_queryset.values_list('employee', flat=True), date=today)

    total_purchases = reports.aggregate(total=models.Sum('amount'))['total'] or 0

    return render(request, 'products/daily_purchase_report.html', {
        'reports': reports,
        'total_purchases': total_purchases,
    })

@login_required(login_url="/accounts/login/")
def absence_report(request):
    """Generate absence report for the logged-in user's store."""
    if request.user.is_admin or request.user.is_superuser:
        employee_queryset = Employee.objects.filter(admin=request.user)  # Get employees managed by the admin
        # Ensure we're filtering with CustomUser instances
        reports = AbsenceReport.objects.filter(employee__in=employee_queryset.values_list('employee', flat=True))
    else:
        employee_queryset = Employee.objects.filter(employee=request.user)  # Get the logged-in employee instance
        reports = AbsenceReport.objects.filter(employee__in=employee_queryset.values_list('employee', flat=True))

    return render(request, 'products/absence_report.html', {'reports': reports})

@login_required(login_url="/accounts/login/")
def overall_report(request):
    """Generate an overall report combining sales, purchases, and absences."""
    if request.user.is_admin or request.user.is_superuser:
        employee_queryset = Employee.objects.filter(admin=request.user)  # Get employees managed by the admin
        # Ensure we're filtering with CustomUser instances
        sales_reports = SalesReport.objects.filter(employee__in=employee_queryset.values_list('employee', flat=True))
        purchase_reports = PurchaseReport.objects.filter(employee__in=employee_queryset.values_list('employee', flat=True))
        absence_reports = AbsenceReport.objects.filter(employee__in=employee_queryset.values_list('employee', flat=True))
    else:
        employee_queryset = Employee.objects.filter(employee=request.user)  # Get the logged-in employee instance
        sales_reports = SalesReport.objects.filter(employee__in=employee_queryset.values_list('employee', flat=True))
        purchase_reports = PurchaseReport.objects.filter(employee__in=employee_queryset.values_list('employee', flat=True))
        absence_reports = AbsenceReport.objects.filter(employee__in=employee_queryset.values_list('employee', flat=True))

    total_sales = sales_reports.aggregate(total=models.Sum('amount'))['total'] or 0
    total_purchases = purchase_reports.aggregate(total=models.Sum('amount'))['total'] or 0

    return render(request, 'products/overall_report.html', {
        'sales_reports': sales_reports,
        'purchase_reports': purchase_reports,
        'absence_reports': absence_reports,
        'total_sales': total_sales,
        'total_purchases': total_purchases,
    })