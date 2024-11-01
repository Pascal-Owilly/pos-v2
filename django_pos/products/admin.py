from django.contrib import admin


from .models import Category, Product, Store, Purchase, Vendor, StoreInventory

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Store)
admin.site.register(Purchase)
admin.site.register(Vendor)
admin.site.register(StoreInventory)
