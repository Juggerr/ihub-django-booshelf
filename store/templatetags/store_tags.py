from django import template


register = template.Library()

@register.filter(name='call')
def callMethod(obj, methodName):
    method = getattr(obj, methodName)

    if obj.__dict__.has_key("__callArg"):
        ret = method(*obj.__callArg)
        del obj.__callArg
        return ret
    return method()


@register.filter(name='args')
def args(obj, arg):
    if not obj.__dict__.has_key("__callArg"):
        obj.__callArg = []

    obj.__callArg += [arg]
    return obj
 

@register.filter(name='get_total_price')
def get_total_price(shoppingcartitem_list):
   return sum([sc.book.price for sc in shoppingcartitem_list ])
   
   
@register.filter(name='get_total_price_order')
def get_total_price_order(order_list):
   return sum([order.total_price for order in order_list ])
   

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})