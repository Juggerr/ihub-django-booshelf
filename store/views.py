from django.shortcuts import render, redirect
from django.forms import ModelForm 
from django.core.urlresolvers import reverse
from django.views.generic import (
    ListView, CreateView, DetailView, RedirectView,
    UpdateView,
)
from .models import Book, ShoppingCartItem, User, Order


class BookListView(ListView):
    model = Book
    paginate_by = 5
    

class BookDetailView(DetailView):
    model = Book


class UserDetailView(DetailView):
    model = User


class OrderListView(ListView):
    model = Order
    
    def get_queryset(self):
        user = self.request.user
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(user=user)


class ShoppingCartListView(ListView):
    model = ShoppingCartItem
    
    def get_queryset(self):
        user = self.request.user
        queryset = super(ShoppingCartListView, self).get_queryset()
        return queryset.filter(user=user)

class BookAddView(RedirectView):
    
    url = '/'
        
    def post(self, request, *args, **kwargs):
        book_pk = request.POST.get('book_id')
        user = User.objects.get(pk=request.user.pk)
        book = Book.objects.get(pk=book_pk)
        ShoppingCartItem.objects.create(user=user, book=book)
        return super(BookAddView, self).get(self, request, *args, **kwargs)

def checkout_view(request):
    Order.objects.create(
        user=request.user,
        total_price=request.user.userinfo.shopping_cart_total_price
    )
    return redirect(reverse('orders'))


def shopping_cart_delete_view(request, pk):
    ShoppingCartItem.objects.filter(user=request.user, pk=pk).delete()
    return redirect(reverse('shopping-cart'))
    

def delete_book_from_cart(request, book_id):
    book = Book.objects.get(book_id=book_id)
    book.delete()
    success_msg = "Sucess"
    return render(request, template_name, context={'success_msg': success_msg})


class BookUpdateView(UpdateView):
    model = Book
    success_url = '/'
    fields = ('title', 'author', 'description', 'price',
              'amazon_id', 'isbn')
    
class BookCreateView(CreateView):
    model = Book
    success_url = '/'
    fields = ('title', 'author', 'description', 'price',
              'amazon_id', 'isbn')
              


