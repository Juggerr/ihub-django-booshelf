from django.db import models
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from django.contrib.auth.models import User 
from django.dispatch import receiver


class UserInfo(models.Model):
    user = models.OneToOneField(User)
        
    def has_book_in_shopping_cart(self, book):
        return self.user.shoppingcartitem_set.filter(book=book).exists()
                         
    @property
    def shopping_cart_total_price(self):
        return sum([sc.book.price for sc in self.user.shoppingcartitem_set.all()])

    @property
    def shopping_cart_items_amount(self):
        return len(self.user.shoppingcartitem_set.all())


class Book(models.Model):
    title = models.CharField(
        max_length=255
    )
    author = models.CharField(
        max_length=150
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=6, decimal_places=2
    )
    pub_date = models.DateField(
        null=True, blank=True
    )
    amazon_id = models.CharField(
        max_length=50, unique=True,
        validators=[RegexValidator(r'[\d\-]+')],
        blank=True,
    )
    isbn = models.CharField(
        max_length=12, unique=True,
        validators=[RegexValidator(r'[\dA-Z]+')]
    )
    
    def __unicode__(self):
        return self.title

class ChangeTimeMixin(models.Model):
    
    created_at = models.DateTimeField(
        auto_now_add=True, 
        null=True, blank=True
    )
    updated_at = models.DateTimeField(
        null=True, blank=True
    )

    class Meta:
        abstract = True

class ShoppingCartItem(ChangeTimeMixin):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return "{} {}".format(self.user, self.book)
    
class Review(ChangeTimeMixin):
    text = models.TextField()
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    
    def belongs_to_user(self, user):
        return user.pk == self.user.pk
     
    def __unicode__(self):
        return "{} | {}".format(self.user, self.text[:120])

class Order(ChangeTimeMixin):
    user = models.ForeignKey(User)
    total_price = models.DecimalField(
        max_digits=6, decimal_places=2
    )

    def __unicode__(self):
        return unicode(self.user)
        
class OrderItem(ChangeTimeMixin):
    order = models.ForeignKey(Order)
    book = models.ForeignKey(Book)

    def __unicode__(self):
        return unicode(self.book)

@receiver(post_save, sender=Order)
def create_items(instance, **kwargs):
    user = instance.user
    shoppingcartitems = user.shoppingcartitem_set.all()
    for sc_item in shoppingcartitems:
        order_item = OrderItem.objects.create(
            book=sc_item.book, order=instance
        )
    shoppingcartitems.delete()
    