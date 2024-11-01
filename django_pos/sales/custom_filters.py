from django import template

register = template.Library()

@register.filter
def total_amount(sales):
    return sum(sale.grand_total for sale in sales)
