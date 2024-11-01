from django.urls import path

from . import views
from sales.views import daily_reports, product_report
from products import views as report_views
from products.views import store_inventory_view, vendors_list

app_name = "products"

urlpatterns = [
    # List categories
    path('categories', views.CategoriesListView, name='categories_list'),
    # Add category
    path('categories/add', views.CategoriesAddView, name='categories_add'),
    # Update category
    path('categories/update/<str:category_id>',
         views.CategoriesUpdateView, name='categories_update'),
    # Delete category
    path('categories/delete/<str:category_id>',
         views.CategoriesDeleteView, name='categories_delete'),

    # List products
    path('', views.ProductsListView, name='products_list'),
    # Add product
    path('add', views.ProductsAddView, name='products_add'),
    # Update product
    path('update/<str:product_id>',
         views.ProductsUpdateView, name='products_update'),
    # Delete product
    path('delete/<str:product_id>',
         views.ProductsDeleteView, name='products_delete'),
    # Get products AJAX
    path("get", views.GetProductsAJAXView, name="get_products"),

    # Add products
    path('add_purchase/', views.add_purchase, name='add_purchase'),  # Make sure to have a trailing slash here

    # List purchases
    path('purchases/', views.purchase_list, name='purchase_list'),  
    path('stores/', views.store_list, name='store_list'),  
    path('store/<int:store_id>/inventory/', store_inventory_view, name='store_inventory'),
    path('vendors/', vendors_list, name='vendors_list'),  

    path('stores/add/', views.add_store, name='add_store'),
    path('vendors/add/', views.add_vendor, name='add_vendor'),
#     path('product-reports/', product_report, name='product_reports'),
#     path('reports/', views.reports, name='reports'), 
#     path('employee_reports/', views.employee_reports, name='employee_reports'),
#     path('sales_reports/', daily_reports, name='daily_reports'),
#     path('bp_vs_sl_reports/', views.bp_vs_sl_reports, name='bp_vs_sl_reports'),
#     path('wastage_reports/', views.wastage_reports, name='wastage_reports'),

    path('reports/daily-sales/', report_views.daily_sales_report, name='daily_sales_report'),
    path('reports/daily-purchases/', report_views.daily_purchase_report, name='daily_purchase_report'),
    path('reports/absences/', report_views.absence_report, name='absence_report'),
    path('reports/overall/', report_views.overall_report, name='overall_report'),

]
