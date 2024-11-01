from django import forms
from products.models import Purchase
from sales.models import SaleDetail

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['product', 'vendor', 'store', 'quantity']

class SaleDetailForm(forms.ModelForm):
    class Meta:
        model = SaleDetail
        fields = ['product', 'quantity']
