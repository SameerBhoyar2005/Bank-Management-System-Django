from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True,auto_created=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique= True)
    pin = models.IntegerField()
    amount = models.IntegerField()

class Transactions(models.Model):
    account = models.ForeignKey(User,related_name='transactions',on_delete=models.PROTECT)

    TRANSACTION_TYPES=[
        ('DEPOSIT','deposit'),
        ('WITHDRAW', 'withdraw'),
        ('TRANSFER', 'transfer')
    ]
    transaction_type = models.CharField(choices=TRANSACTION_TYPES)

    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"



