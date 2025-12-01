from django.db import models
from accounts.models import Account
from book.models import Books

# DIVISION_CHOICES = [
#     ('baku', 'Bakı'),
#     ('ganja', 'Gəncə'),
#     ('sumgait', 'Sumqayıt'),
# ]
#
#
PAYMENT_METHOD_CHOICES = [
    ('bkash', 'Bkash'),
    ('nagad', 'Nagad'),
    ('cod', 'Cash on delivery'),
]


class Division(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    address = models.CharField(max_length=250)
    division = models.ForeignKey(Division, on_delete=models.CASCADE) # bölgə
    district = models.ForeignKey(District, on_delete=models.CASCADE) # rayon
    zip_code = models.CharField(max_length=30) # poçt indeksi
    payment_method = models.CharField(max_length=20,choices=PAYMENT_METHOD_CHOICES)
    account_no = models.CharField(max_length=25)
    transaction_id = models.IntegerField()
    payable = models.FloatField() # ümumi ödəniləcək məbləğ
    totalbook = models.IntegerField() # sifarişte neçə kitab var
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False) # Sifariş ödənilib?

    def __str__(self):
        return 'Order {}'.format(self.id) #  return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.price * item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_total(self):
        return self.price * self.quantity


