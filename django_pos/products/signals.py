# from django.db.models.signals import post_save, pre_delete
# from django.dispatch import receiver
# from .models import Purchase, StoreInventory
# from sales.models import SaleDetail

# @receiver(post_save, sender=Purchase)
# def update_inventory_on_purchase(sender, instance, created, **kwargs):
#     if created:
#         store_inventory, created = StoreInventory.objects.get_or_create(store=instance.store, product=instance.product)
#         store_inventory.quantity += instance.quantity
#         store_inventory.save()
#         print(f"Inventory updated for purchase: {instance.product.name} at {instance.store.name}")

# @receiver(post_save, sender=SaleDetail)
# def update_inventory_on_sale(sender, instance, created, **kwargs):
#     if created:
#         try:
#             store_inventory = StoreInventory.objects.get(store=instance.sale.store, product=instance.product)
#             store_inventory.quantity -= instance.quantity
#             if store_inventory.quantity <= 0:
#                 store_inventory.delete()
#             else:
#                 store_inventory.save()
#             print(f"Inventory updated for sale: {instance.product.name} at {instance.sale.store.name}")
#         except StoreInventory.DoesNotExist:
#             pass  # Handle the case where inventory record does not exist if necessary

# @receiver(pre_delete, sender=SaleDetail)
# def revert_inventory_on_sale_delete(sender, instance, **kwargs):
#     try:
#         store_inventory = StoreInventory.objects.get(store=instance.sale.store, product=instance.product)
#         store_inventory.quantity += instance.quantity
#         store_inventory.save()
#         print(f"Inventory reverted for sale deletion: {instance.product.name} at {instance.sale.store.name}")
#     except StoreInventory.DoesNotExist:
#         pass  # Handle the case where inventory record does not exist if necessary
