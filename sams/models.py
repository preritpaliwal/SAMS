from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class ShowManager(models.Model):
    # USER_TYPE=(('manager','manager'),('sales','sales'),('clerk','clerk'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=True)
    # user_type=models.CharField(max_length=10,choices=USER_TYPE,default='sales')


class Salesperson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # show=models.ForeignKey(Show,on_delete=models.CASCADE,null=True,blank=True)
    is_salesperson = models.BooleanField(default=True)
    total_commission = models.IntegerField(null=True, blank=True, default=0)
    percent_commission = models.IntegerField(null=True, blank=True, default=0)
    amount_collected = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.user.username


class Show(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    # salesperson = models.ForeignKey(
    #     Salesperson, on_delete=models.CASCADE, null=True, blank=True)  # send id of the sales person
    total_bal = models.IntegerField(null=True, blank=True)
    total_ord = models.IntegerField(null=True, blank=True)
    price_bal = models.FloatField(null=True, blank=True)
    price_ord = models.FloatField(null=True, blank=True)
    available_bal = models.IntegerField(null=True, blank=True)
    available_ord = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TType=(('debit','debit'),('credit','credit'))

    transaction_type=models.CharField(max_length=100,choices=TType, null=True, blank=True)
    amount=models.IntegerField(null=True, blank=True,default=0)
    desc = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField(
        default=datetime.datetime.now(), null=True, blank=True)
    


class Clerk(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    balance_sheet = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, null=True, blank=True)
    is_clerk = models.BooleanField(default=True)


class Ticket(models.Model):
    TICKET_TYPES = (('BAL', 'BAL'), ('ORD', 'ORD'), ('VIP', 'VIP'))
    type = models.CharField(
        max_length=50, choices=TICKET_TYPES, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    salesperson = models.ForeignKey(
        Salesperson, on_delete=models.CASCADE, null=True, blank=True)
    show = models.ForeignKey(
        Show, on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField(default=0)
    salescommission = models.IntegerField(default=0)
    seat = models.IntegerField(null=True, blank=True)

class Expenditure(models.Model):
    TType=(('debit','debit'),('credit','credit'))
    # name = models.CharField(max_length=100, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    amount=models.IntegerField(default=0)
    transaction_type=models.CharField(max_length=100,choices=TType, null=True, blank=True)
    show=models.ForeignKey(Show,on_delete=models.CASCADE,null=True,blank=True)
# class Spectator(models.Model):
#     name = models.CharField(max_length=50,null=True,blank=True)
#     ticket=models.ForeignKey(Ticket,on_delete=models.CASCADE,null=True,blank=True)
