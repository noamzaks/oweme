from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from .models import Coin, Payers, Debts

def home(request):
    return render(request, "home.html", {})

def purchase(request, group_name=None):
    if request.method == "POST":
        if "amount" in request.POST:
            new_coin = Coin(user=request.user, amount=float(request.POST["amount"]))
            new_coin.save()
            return redirect(request.path)

    users = None
    users_with_coins = None
    if group_name and request.user.is_authenticated:
        payers = Payers.objects.get_or_create(name=group_name)[0]

        users = payers.users.all()

        if not request.user in users:
            payers.users.add(request.user)
            payers.save()

        debts_from_before = []

        for user in users:
            for other in users:
                debts = Debts.objects.filter(one=user, two=other) | Debts.objects.filter(one=other,two=other)
                if debts.exists():
                    debts_from_before.append(debts[0])

        users_with_coins = {}
        for user in users:
            users_with_coins[user] = [ float(coin.amount) for coin in user.coin_set.all() ]

        users_with_coins = users_with_coins.items()

    return render(request, "purchase.html", {
        "group_name": group_name,
        "users": users_with_coins,
    })

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"