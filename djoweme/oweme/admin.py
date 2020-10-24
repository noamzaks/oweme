from django.contrib import admin

from .models import Payers, Debts, Coin

admin.site.register(Payers)
admin.site.register(Debts)
admin.site.register(Coin)