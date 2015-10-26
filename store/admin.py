from django.contrib import admin
from store.models import (
    Book, ShoppingCartItem, Review, 
    Order, OrderItem, UserInfo,
)

admin.site.register(UserInfo)
admin.site.register(Book)
admin.site.register(ShoppingCartItem)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
