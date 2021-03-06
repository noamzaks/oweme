from django.http.response import HttpResponse
from oweme.debt_circles import fix
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic

from .models import Coin, Payers, Debts, PayDebt, Bill
from .oweme import howToPay

@login_required(login_url="/accounts/login")
def debts(request):
    debts = Debts.objects.filter(one=request.user) | Debts.objects.filter(two=request.user)
    
    return render(request, "debts.html", {
        "debts": debts,
    })

def home(request):
    pay_debt_requests = None
    mini,loop = None, None
    if request.user.is_authenticated:
        pay_debt_requests = PayDebt.objects.filter(two=request.user)

        if request.method == "POST":
            if "answer_request" in request.POST and "debt" in request.POST:
                req = pay_debt_requests.filter(id=request.POST["debt"])
                if req.exists():
                    req = req.first()
                    if request.POST["answer_request"] == "accept":
                        debts = Debts.objects.filter(one=request.user, two=req.one) | Debts.objects.filter(one=req.one, two=request.user)
                        new_debt = -req.amount
                        for debt in debts:
                            if debt.one == request.user:
                                new_debt -= debt.amount
                            else:
                                new_debt += debt.amount
                        debts.delete()
                        if new_debt < 0:
                            Debts(one=request.user, two=req.one, amount=-new_debt).save()
                        elif new_debt > 0:
                            Debts(one=req.one, two=request.user, amount=new_debt).save()
                        mini,loop = fix(request.user, req.one)
                    req.delete()

    return render(request, "home.html", {
        "pay_debt_requests": pay_debt_requests,
        "mini": mini,
        "loop": loop,
    })

def pay_debt(request):
    if request.method == "POST":
        success = True
        if "user" in request.POST and "amount" in request.POST:
            to = request.POST["user"]
            user = User.objects.filter(username=to)
            if user.exists():
                user = user.first()
                if not PayDebt.objects.filter(one=request.user, two=user).exists():
                    PayDebt(one=request.user, two=user, amount=request.POST["amount"]).save()
                    success = True
        return redirect(request.path + f"?success={success}")

    sent = None
    if "success" in request.GET:
        sent = request.GET["success"]

    return render(request, "pay-debt.html", {
        "sent": sent,
    })
    
@login_required(login_url="/accounts/login")
def purchase(request, group_name=None):
    users = None
    users_with_coins = {}
    bills = None
    debts_from_before = None
    bill_dict = {}
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


        bills = Bill.objects.filter(user__in=users)
        
        bill_dict = {}
                
        for bill in bills:
            bill_dict[bill.user] = bill.value
            
    if request.method == "POST":
        if "amount" in request.POST:
            if "bill" not in request.POST:
                new_coin = Coin(user=request.user, amount=float(request.POST["amount"]))
                new_coin.save()
            else:
                bill = Bill.objects.filter(user=request.user)
                if bill.exists():
                    bill = bill.first()
                    bill.value = float(request.POST["amount"])
                    bill.save()
                else:
                    new_bill = Bill(user=request.user, value=float(request.POST["amount"]))
                    new_bill.save()
        if "coin" in request.POST:
            matching_coins = Coin.objects.filter(user=request.user, amount=float(request.POST["coin"]))
            if matching_coins.exists():
                matching_coins.first().delete()
        if "complete_purchase" in request.POST:
            x = howToPay(users, debts_from_before, users_with_coins, bill_dict)
            for debt in debts_from_before:
                debt.delete()

            Coin.objects.filter(user__in=users).delete()
            
            if x == -1:
                return HttpResponse("<h1>Yer be broke, bros!</h1>")
            
            return render(request, "after-purchase.html", {
                "x": x[0].items(),
                "y": x[1],
                "z": x[2],
            })
        return redirect(request.path)
    
    return render(request, "purchase.html", {
        "group_name": group_name,
        "users": users_with_coins.items(),
        "bill_dict": bill_dict.items(),
    })

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"