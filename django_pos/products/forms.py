# forms.py
from django import forms
from .models import Purchase, Store, Vendor

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['store', 'product','vendor', 'quantity']

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name','location', 'contact']  # Add other fields as needed

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'contact_info', 'address']  # Add other fields as needed
    