from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PurchaseForm
import json
from django.db.models import Sum, F
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_pos.wsgi import *
from django_pos import settings
from django.template.loader import get_template
from customers.models import Customer
from products.models import Product
from weasyprint import HTML, CSS
from .models import Sale, SaleDetail
import json
from products.models import StoreInventory, Store, Product
from django.http import JsonResponse

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url="/accounts/login/")
def purchase_list(request):
    purchases = Purchase.objects.all()
    return render(request, 'products/purchase_list.html', {'purchases': purchases})


@login_required(login_url="/accounts/login/")
def add_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)  # Don't save to database yet
            purchase.save()  # Save the purchase to get its ID

            # Update product quantity in the Store model
            store = purchase.store
            product = purchase.product
            quantity = purchase.quantity

            store.update_product_quantity(product_id=product.id, quantity=quantity)

            return redirect('products:purchase_list')
    else:
        form = PurchaseForm()
    return render(request, 'products/add_purchase.html', {'form': form})

@login_required(login_url="/accounts/login/")
def SalesListView(request):
    # Get all sales
    sales = Sale.objects.all().order_by('-date_added')

    # Calculate total amount for each sale
    for sale in sales:
        total_amount = SaleDetail.objects.filter(sale=sale).aggregate(total_amount=Sum('total_detail'))['total_amount']
        sale.total_amount = total_amount or 0  # Set total amount to 0 if no sale details found

    context = {
        "active_icon": "sales",
        "sales": sales
    }
    return render(request, "sales/sales.html", context=context)

from django.db import transaction

@login_required(login_url="/accounts/login/")
def SalesAddView(request):
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Save the POST arguments
            data = json.loads(request.body)

            sale_attributes = {
                "customer": Customer.objects.get(id=int(data.get('customer'))),
                "sub_total": float(data.get("sub_total")),
                "grand_total": float(data.get("grand_total")),
                "tax_amount": float(data.get("tax_amount")),
                "tax_percentage": float(data.get("tax_percentage")),
                "amount_payed": float(data.get("amount_payed")),
                "amount_change": float(data.get("amount_change")),
            }

            # Use Django's transaction atomic block to ensure data consistency
            with transaction.atomic():
                try:
                    # Create the sale
                    new_sale = Sale.objects.create(**sale_attributes)
                    
                    # Create the sale details
                    products = data.get("products")

                    for product in products:
                        detail_attributes = {
                            "sale": new_sale,
                            "product": Product.objects.get(id=int(product.get("id"))),
                            "price": product.get("price"),
                            "quantity": product.get("quantity"),
                            "total_detail": product.get("total_product")
                        }
                        SaleDetail.objects.create(**detail_attributes)

                        # Update the store's inventory
                        store = Store.objects.get(id=int(product.get("store_id"))).order_by('-date_created')
                        product_id = int(product.get("id"))
                        quantity_sold = int(product.get("quantity"))
                        update_store_inventory(store, product_id, quantity_sold)

                    messages.success(
                        request, 'Sale created successfully!', extra_tags="success")

                except Exception as e:
                    messages.error(
                        request, 'There was an error during the creation!', extra_tags="danger")

                return JsonResponse({"redirect_url": "/sales/list/"})

    context = {
        "active_icon": "sales",
        "customers": [c.to_select2() for c in Customer.objects.all()],
        "stores": Store.objects.all()
    }

    return render(request, "sales/sales_add.html", context=context)

def update_store_inventory(store, product_id, quantity_sold):
    """
    Update the store's inventory after a sale.
    """
    try:
        # Retrieve the store inventory entry for the product
        store_inventory = StoreInventory.objects.get(store=store, product_id=product_id)
        
        # Deduct the sold quantity from the store's inventory
        store_inventory.quantity -= quantity_sold
        store_inventory.save()

        print(f"Updated store inventory for product ID {product_id} in store {store.name} to {store_inventory.quantity}.")
    except StoreInventory.DoesNotExist:
        # Handle case where the product is not found in the store's inventory
        print(f"Product ID {product_id} not found in store {store.name} inventory.")

@login_required(login_url="/accounts/login/")
def SalesDetailsView(request, sale_id):
    try:
        sale = Sale.objects.get(id=sale_id)
        details = SaleDetail.objects.filter(sale=sale).order_by('-date_added')

        context = {
            "active_icon": "sales",
            "sale": sale,
            "details": details,
        }
        return render(request, "sales/sales_details.html", context=context)
    except Exception as e:
        messages.error(request, 'There was an error getting the sale!', extra_tags="danger")
        return redirect('sales:sales_list')

# Reports
@login_required(login_url="/accounts/login/")
def daily_reports(request):
    # Get today's date
    today = datetime.now().date()

    # Calculate the date for yesterday
    yesterday = today - timedelta(days=1)

    # Calculate the last 7 days
    last_seven_days = [today - timedelta(days=i) for i in range(7)]

    # Get the selected date from the query parameters
    selected_date_str = request.GET.get('date')
    selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date() if selected_date_str else today

    # Get sales data for the selected day
    selected_day_sales = SaleDetail.objects.filter(sale__date_added__date=selected_date).select_related('product').annotate(
        total_quantity=Sum('quantity'),
        total_amount=Sum('total_detail')
    )

    context = {
        'today': today,
        'yesterday': yesterday,
        'last_seven_days': last_seven_days,
        'selected_date': selected_date,
        'selected_day_sales': selected_day_sales,
    }

    return render(request, 'products/sales_reports.html', context)

@login_required(login_url="/accounts/login/")
def product_report(request):
    # Retrieve all products
    products = Product.objects.all()

    # Create a dictionary to hold current stock values
    product_stock = {}

    # Calculate the current stock for each product from all stores
    stores = Store.objects.all()
    for store in stores:
        try:
            product_quantities = json.loads(store.product_quantities)
            for product_id, quantity in product_quantities.items():
                if product_id in product_stock:
                    product_stock[product_id] += quantity
                else:
                    product_stock[product_id] = quantity
        except json.JSONDecodeError:
            # Handle JSON decoding error, you can log this error or print it for debugging
            print(f"Error decoding JSON for store {store.id}: {store.product_quantities}")

    # Annotate each product with the total quantity sold and current stock
    products = products.annotate(
        total_sales=Sum('saledetail__quantity')
    )

    # Add current stock to each product
    for product in products:
        product.current_stock = product_stock.get(str(product.id), 0)

    context = {
        'products': products,
    }

    return render(request, 'products/product_reports.html', context)


@login_required(login_url="/accounts/login/")
def ReceiptPDFView(request, sale_id):
    """
    Args:
        sale_id: ID of the sale to view the receipt
    """
    # Get tthe sale
    sale = Sale.objects.get(id=sale_id)

    # Get the sale details
    details = SaleDetail.objects.filter(sale=sale)

    template = get_template("sales/sales_receipt_pdf.html")
    context = {
        "sale": sale,
        "details": details
    }
    html_template = template.render(context)

    # CSS Boostrap
    css_url = os.path.join(
        settings.BASE_DIR, 'static/css/receipt_pdf/bootstrap.min.css')

    # Create the pdf
    pdf = HTML(string=html_template).write_pdf(stylesheets=[CSS(css_url)])

    return HttpResponse(pdf, content_type="application/pdf")


