from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Customer, Supplier


@login_required(login_url="/accounts/login/")
def CustomersListView(request):
    context = {
        "active_icon": "customers",
        "customers": Customer.objects.all().order_by('-date_added')
    }
    return render(request, "customers/customers.html", context=context)


@login_required(login_url="/accounts/login/")
def CustomersAddView(request):
    context = {
        "active_icon": "customers",
    }

    if request.method == 'POST':
        # Save the POST arguements
        data = request.POST

        attributes = {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "address": data['address'],
            "email": data['email'],
            "phone": data['phone'],
        }

        # Check if a customer with the same attributes exists
        if Customer.objects.filter(**attributes).exists():
            messages.error(request, 'Customer already exists!',
                           extra_tags="warning")
            return redirect('customers:customers_add')

        try:
            # Create the customer
            new_customer = Customer.objects.create(**attributes)

            # If it doesn't exists save it
            new_customer.save()

            messages.success(request, 'Customer: ' + attributes["first_name"] + " " +
                             attributes["last_name"] + ' created succesfully!', extra_tags="success")
            return redirect('customers:customers_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('customers:customers_add')

    return render(request, "customers/customers_add.html", context=context)


@login_required(login_url="/accounts/login/")
def CustomersUpdateView(request, customer_id):
    """
    Args:
        customer_id : The customer's ID that will be updated
    """

    # Get the customer
    try:
        # Get the customer to update
        customer = Customer.objects.get(id=customer_id)
    except Exception as e:
        messages.success(
            request, 'There was an error trying to get the customer!', extra_tags="danger")
        print(e)
        return redirect('customers:customers_list')

    context = {
        "active_icon": "customers",
        "customer": customer,
    }

    if request.method == 'POST':
        try:
            # Save the POST arguements
            data = request.POST

            attributes = {
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "address": data['address'],
                "email": data['email'],
                "phone": data['phone'],
            }

            # Check if a customer with the same attributes exists
            if Customer.objects.filter(**attributes).exists():
                messages.error(request, 'Customer already exists!',
                               extra_tags="warning")
                return redirect('customers:customers_add')

            # Get the customer to update
            customer = Customer.objects.filter(
                id=customer_id).update(**attributes)

            customer = Customer.objects.get(id=customer_id)

            messages.success(request, '¡Customer: ' + customer.get_full_name() +
                             ' updated successfully!', extra_tags="success")
            return redirect('customers:customers_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the update!', extra_tags="danger")
            print(e)
            return redirect('customers:customers_list')

    return render(request, "customers/customers_update.html", context=context)


@login_required(login_url="/accounts/login/")
def CustomersDeleteView(request, customer_id):
    """
    Args:
        customer_id : The customer's ID that will be deleted
    """
    try:
        # Get the customer to delete
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        messages.success(request, '¡Customer: ' + customer.get_full_name() +
                         ' deleted!', extra_tags="success")
        return redirect('customers:customers_list')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('customers:customers_list')

# Suppliers
@login_required(login_url="/accounts/login/")
def SuppliersListView(request):
    context = {
        "active_icon": "suppliers",
        "suppliers": Supplier.objects.all().order_by('-date_added')
    }
    return render(request, "customers/suppliers.html", context=context)


@login_required(login_url="/accounts/login/")
def SuppliersAddView(request):
    context = {
        "active_icon": "suppliers",
    }

    if request.method == 'POST':
        # Save the POST arguements
        data = request.POST

        attributes = {
            "name": data['name'],
            "address": data['address'],
            "email": data['email'],
            "phone": data['phone'],
        }

        # Check if a customer with the same attributes exists
        if Supplier.objects.filter(**attributes).exists():
            messages.error(request, 'Supplier already exists!',
                           extra_tags="warning")
            return redirect('customers:suppliers_add')

        try:
            # Create the customer
            new_supplier = Supplier.objects.create(**attributes)

            # If it doesn't exists save it
            new_supplier.save()

            messages.success(request, 'Supplier: ' + attributes["name"] + " " +
                             ' created succesfully!', extra_tags="success")
            return redirect('customers:suppliers_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('customers:suppliers_add')

    return render(request, "customers/suppliers_add.html", context=context)


@login_required(login_url="/accounts/login/")
def SuppliersUpdateView(request, supplier_id):
    """
    Args:
        csupplier_id : The csuppliersr's ID that will be updated
    """

    # Get the customer
    try:
        # Get the customer to update
        supplier = Supplier.objects.get(id=supplier_id)
    except Exception as e:
        messages.success(
            request, 'There was an error trying to get the supplier!', extra_tags="danger")
        print(e)
        return redirect('customers:suppliers_list')

    context = {
        "active_icon": "suppliers",
        "supplier": supplier,
    }

    if request.method == 'POST':
        try:
            # Save the POST arguements
            data = request.POST

            attributes = {
                "name": data['name'],
                "address": data['address'],
                "email": data['email'],
                "phone": data['phone'],
            }

            # Check if a customer with the same attributes exists
            if Supplier.objects.filter(**attributes).exists():
                messages.error(request, 'Supplier already exists!',
                               extra_tags="warning")
                return redirect('customers:suppliers_add')

            # Get the customer to update
            suppliers = Supplier.objects.filter(
                id=supplier_id).update(**attributes)

            supplier = Supplier.objects.get(id=supplier_id)

            messages.success(request, '¡Customer: ' + supplier.name +
                             ' updated successfully!', extra_tags="success")
            return redirect('customers:suppliers_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the update!', extra_tags="danger")
            print(e)
            return redirect('customers:suppliers_list')

    return render(request, "customers/suppliers_update.html", context=context)


@login_required(login_url="/accounts/login/")
def SuppliersDeleteView(request, supplier_id):
    """
    Args:
       supplier_id : The supplier's ID that will be deleted
    """
    try:
        # Get the customer to delete
        supplier = Supplier.objects.get(id=supplier_id)
        supplier.delete()
        messages.success(request, 'Suppliers: ' + supplier.name +
                         ' deleted!', extra_tags="success")
        return redirect('customers:suppliers_list')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('customers:suppliers_list')

