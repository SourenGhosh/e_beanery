from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class UserSetting(models.Model):
    USER_CHOICES = (
        ("customer", "Customer"),
        ("resturant_manager", "Resturant Manager"),
        ("chef", "Chef"),
        ("waiter", "Waiter")
    )
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name="user_setting")
    user_type = models.CharField(max_length = 20, choices = USER_CHOICES, null=True, blank = True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} | {self.user_type}"

class MealType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


class Table(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self, *args, **kwargs):
        return self.name



# class Customer(models.model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=20, null=True, blank=True)



class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    order_status = (
        ("order_placed", "Order Placed"),
        ("being_cooked", "Being Cooked"),
        ("delivered", "Delivered"),
        ("closes", "Closed"),
        ("cancelled", "Cancelled"),
    )
    id = models.AutoField(primary_key=True)
    table = models.ManyToManyField(Table)
    customer = models.ForeignKey(UserSetting, on_delete = models.PROTECT)
    meal_type = models.ForeignKey(MealType, on_delete = models.PROTECT)
    status = models.CharField(max_length=30, choices = order_status, default = order_status[0][0])
    expected_arrival = models.DateTimeField(default = datetime.now()+timedelta(minutes=30))

    def __str__(self):
        return f"{self.id} | {self.customer.user.first_name}"

    @property
    def customer_name(self):
        return self.customer.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        tables = self.table.all() 
        for table in tables:
            table.is_booked = True   #book table for each successfull order
            table.save()


class BillingDetails(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.OneToOneField(Order, on_delete = models.CASCADE, related_name="order_bill")
    amount = models.FloatField(default=0.0)
    is_paid = models.BooleanField(default=False)
    is_refunded = models.BooleanField(default=False)
    order_delay_time = models.FloatField(default=0.0)

    @property
    def customer_name(self, *args, **kwargs):
        self.order.customer_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        tables = self.order.table.all()
        for table in tables:
            table.is_booked = False #upon sccessfull payment release the table
            table.save()
        

    def __str__(self):
        return self.id

class STATUS:
    OPEN = "Open"
    IN_REVIEW = "In_Review"
    ACCEPTED = "Accepted"
    CANCELLED = "Cancelled"
    CLOSED = "Closed"


class AddressReversal(models.Model):
    STATUS_CHOICES = (
        (STATUS.OPEN, "Open"),
        (STATUS.IN_REVIEW, "In Review"),
        (STATUS.ACCEPTED, "Accepted"),
        (STATUS.CLOSED, "Closed"),
        (STATUS.CANCELLED, "Cancelled"),
    )

    id = models.AutoField(primary_key=True)
    bill = models.ForeignKey(BillingDetails, on_delete=models.CASCADE)
    customer_feedback = models.TextField(null=True, blank=True)
    has_requested_refunded = models.BooleanField(default=False)
    refund_status = models.CharField(max_length=30, choices = STATUS_CHOICES, default = STATUS_CHOICES[0])


    def __str__(self):
        return f"{self.bill.customer_name} | {self.bill.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
        if self.refund_status == STATUS.CLOSED: #upon refund status accepted it will reflect on billing details instance
            self.bill.is_refunded = True
            self.bill.save()



