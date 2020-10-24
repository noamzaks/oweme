from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from .models import Coin, Payers, Debts, PayDebt

def home(request):
    pay_debt_requests = PayDebt.objects.filter(debt__one=request.user, debt__amount__lt=0) | PayDebt.objects.filter(debt__two=request.user, debt__amount__gt=0)

    if request.method == "POST":
        if "answer_request" in request.POST and "debt" in request.POST:
            req = pay_debt_requests.filter(id=request.POST["debt"])
            if req.exists():
                req = req.first()
                if request.POST["answer_request"] == "accept":
                    req.debt.delete()
                print(req.delete())
        return redirect(request.path)

    return render(request, "home.html", {
        "pay_debt_requests": pay_debt_requests,
    })

def pay_debt(request, to=None):
    debts = Debts.objects.filter(one=request.user, amount__gt=0) | Debts.objects.filter(two=request.user, amount__lt=0)

    if to:
        debt = Debts.objects.filter(one=request.user, two__username=to, amount__gt=0) | Debts.objects.filter(one__username=to, two=request.user, amount__lt=0)
        if debt.exists():
            debt = debt.first()
            if not PayDebt.objects.filter(debt=debt):
                paid = PayDebt(debt=debt)
                paid.save()

    return render(request, "pay-debt.html", {
        "to": to,
        "debts": debts,
    })

def purchase(request, group_name=None):
    if request.method == "POST":
        if "amount" in request.POST:
            new_coin = Coin(user=request.user, amount=float(request.POST["amount"]))
            new_coin.save()
        if "coin" in request.POST:
            matching_coins = Coin.objects.filter(user=request.user, amount=float(request.POST["coin"]))
            if matching_coins.exists():
                matching_coins.first().delete()
        if "complete_purchase" in request.POST:
            print("TBD")
        return redirect(request.path)

    users = None
    users_with_coins = None
    if group_name and request.user.is_authenticated:
        payers = Payers.objects.get_or_create(name=group_name)[0]

        users = payers.users.all()

        if not request.user in users:
            payers.users.add(request.user)
            payers.save()

        users = payers.users.all()

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