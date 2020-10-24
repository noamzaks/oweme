from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Payers(models.Model):
    class Meta:
        verbose_name_plural = "Payers"

    name  = models.CharField(max_length=50)
    users = models.ManyToManyField(User)

class Coin(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(decimal_places=5, max_digits=10)

class Debts(models.Model):
    class Meta:
        verbose_name_plural = "Debts"

    one = models.ForeignKey(User, on_delete=models.DO_NOTHING) # if user is deleted they dont escape their debts lol
    two = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="two")
    amount = models.DecimalField(decimal_places=5, max_digits=10)

class PayDebt(models.Model):
    debt = models.ForeignKey(Debts, on_delete=models.CASCADE)