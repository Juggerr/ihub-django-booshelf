from django.conf.urls import include, url
from django.contrib import admin

from store.views import (
    BookListView, BookDetailView, BookCreateView, UserDetailView,
    OrderListView, ShoppingCartListView, BookAddView, BookUpdateView,
    checkout_view, shopping_cart_delete_view
)

urlpatterns = [
    url(r'^$', BookListView.as_view(), name='index'),
    url(r'^books/$', BookListView.as_view(), name='book-list-search'),
    url(r'^books/(?P<pk>\d+)/$', BookDetailView.as_view(), name='book'),
    url(r'^books/add-to-cart/$', BookAddView.as_view(), name='book-add-to-cart'),
    url(r'^books/add/$', BookCreateView.as_view(), name='book-add'),
    url(r'^books/edit/(?P<pk>\d+)/$', BookUpdateView.as_view(), name='book-edit'),
    url(r'^users/(?P<pk>\d+)/$', UserDetailView.as_view(), name='user-detail'),
    url(r'^orders/$', OrderListView.as_view(), name='orders'),
    url(r'^checkout/$', checkout_view, name='checkout'), 
    url(r'^shopping-cart/$', ShoppingCartListView.as_view(), name='shopping-cart'),
    url(r'^shopping-cart/delete/(?P<pk>\d+)/$', shopping_cart_delete_view, name='shopping-cart-delete'),
    
    url(r'^users/', include('django.contrib.auth.urls')),
    url(r'^users/', include('registration.backends.simple.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
