from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, FloatField, Q
from django.db.models.functions import Coalesce
from sales.models import Sale
from products.models import Product, Category
import json
from datetime import date
from authentication.models import Employee

@login_required(login_url="/accounts/login/")
def index(request):
    today = date.today()
    year = today.year
    monthly_earnings = []

    # Get all employees managed by the logged-in admin
    managed_employees = Employee.objects.filter(admin=request.user)

    # Calculate earnings per month specific to the logged-in admin's employees
    for month in range(1, 13):
        earning = Sale.objects.filter(
            date_added__year=year,
            date_added__month=month,
            employee__in=[emp.employee for emp in managed_employees]  # Filter by managed employees
        ).aggregate(
            total_variable=Coalesce(Sum('grand_total'), 0.0, output_field=FloatField())
        ).get('total_variable', 0)
        monthly_earnings.append(earning)

    # Calculate annual earnings specific to the logged-in admin's employees
    annual_earnings = Sale.objects.filter(
        date_added__year=year,
        employee__in=[emp.employee for emp in managed_employees]  # Filter by managed employees
    ).aggregate(
        total_variable=Coalesce(Sum('grand_total'), 0.0, output_field=FloatField())
    ).get('total_variable', 0)

    annual_earnings = format(annual_earnings, '.2f')

    # Average earnings per month
    avg_month = format(sum(monthly_earnings) / 12, '.2f') if sum(monthly_earnings) > 0 else '0.00'

    # Top selling products specific to the logged-in admin's employees
    top_products = Product.objects.annotate(
        quantity_sum=Sum('saledetail__quantity', filter=Q(saledetail__sale__employee__in=[emp.employee for emp in managed_employees]))
    ).order_by('-quantity_sum')[:3]

    top_products_names = []
    top_products_quantity = []

    for p in top_products:
        top_products_names.append(p.name)
        top_products_quantity.append(p.quantity_sum)

    context = {
        "active_icon": "dashboard",
        "products": Product.objects.filter(user=request.user).count(),
        "categories": Category.objects.all().count(),
        "annual_earnings": annual_earnings,
        "monthly_earnings": json.dumps(monthly_earnings),
        "avg_month": avg_month,
        "top_products_names": json.dumps(top_products_names),
        "top_products_names_list": top_products_names,
        "top_products_quantity": json.dumps(top_products_quantity),
    }
    return render(request, "pos/index.html", context)
