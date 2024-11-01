from django.urls import path

from customers import views

app_name = "customers"
urlpatterns = [
    # List customers
    path('', views.CustomersListView, name='customers_list'),
    # Add customer
    path('add', views.CustomersAddView, name='customers_add'),
    # Update customer
    path('update/<str:customer_id>',
         views.CustomersUpdateView, name='customers_update'),
    # Delete customer
    path('delete/<str:customer_id>',
         views.CustomersDeleteView, name='customers_delete'),
    # List suppliers
    path('suppliers', views.SuppliersListView, name='suppliers_list'),
    # Add supplier
    path('add_supplier', views.SuppliersAddView, name='suppliers_add'),
    # Update supplier
    path('update_supplier/<str:supplier_id>',
         views.SuppliersUpdateView, name='supplier_update'),
    # Delete supplier
    path('delete/<str:supplier_id>',
         views.SuppliersDeleteView, name='suppliers_delete'),
]
