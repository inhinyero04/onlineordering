from django.db import models
from datetime import datetime
from django.utils import timezone
from django.conf import settings

now = timezone.now()

class Member(models.Model):
    code_number = models.CharField(unique=True, max_length=20, verbose_name='Code Number')
    full_name =  models.CharField(max_length=300, verbose_name='Full Name')
    shipping_address =  models.CharField(max_length=200, verbose_name='Shipping Address')
    contact_number =  models.CharField(max_length=20, verbose_name='Contact Number')
    email =  models.CharField(max_length=100, verbose_name='Email')
    password = models.CharField(max_length=50, verbose_name='Password')
    pub_date = models.DateField(default=now)

    class Meta:
        verbose_name_plural = "1. Members"
        ordering = ('full_name',)

    def __str__(self):
        return self.code_number

class Category(models.Model):
    description = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Setup - Category"
        ordering = ('description',)

    def __str__(self):
        return self.description

class BranchSetup(models.Model):
    description = models.CharField(max_length=200, unique=True)
#    region = models.ForeignKey(RegionSetup, on_delete=models.SET_NULL,  null=True, blank=True, related_name='%(class)s_region', verbose_name='Region')

    class Meta:
        verbose_name_plural = "Setup - Branch"
        ordering = ('description',)

    def __str__(self):
        return self.description

class Item(models.Model):
    item_code = models.CharField(unique=True, max_length=100)
    item_name = models.CharField(max_length=100)
    image = models.ImageField()

    class Meta:
        verbose_name_plural = "2. Item"
        ordering = ('item_name',)

    def __str__(self):
        return self.item_name

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    branch =  models.ForeignKey(BranchSetup, on_delete=models.CASCADE,  null=True, blank=True)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "3. Order Item"
    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

#    def check_stock(self):
#        return self


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()

    class Meta:
        verbose_name_plural = "4. Cart"

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Setup - Payment"
