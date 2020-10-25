from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey

# Create your models here.
class Payers(models.Model):
    class Meta:
        verbose_name_plural = "Payers"

    name  = models.CharField(max_length=50)
    users = models.ManyToManyField(User)
    
    def __str__(self):
        return self.name

class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    value = models.DecimalField(decimal_places=5, max_digits=10)

class Coin(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(decimal_places=5, max_digits=10)

    def __str__(self):
        return f"{self.user}'s {self.amount}"

class Debts(models.Model):
    class Meta:
        verbose_name_plural = "Debts"

    one = models.ForeignKey(User, on_delete=models.DO_NOTHING) # if user is deleted they dont escape their debts lol
    two = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="two")
    amount = models.DecimalField(decimal_places=5, max_digits=10)

    def __str__(self):
        return f"{self.one} owes {self.two}: {self.amount}"

class PayDebt(models.Model):
    one = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="payone") # if user is deleted they dont escape their debts lol
    two = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="paytwo")
    amount = models.DecimalField(decimal_places=5, max_digits=10)
    
    def __str__(self):
        return f"{self.one} pays {self.two}: {self.amount}"