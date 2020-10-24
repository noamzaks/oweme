from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from .models import Payers, Debts

def home(request):
    return render(request, "home.html", {})

def purchase(request, group_name=None):
    payers = None
    if group_name:
        payers = Payers.objects.get_or_create(name=group_name)[0]

        users = payers.users.all()

        if not request.user in users:
            payers.users.add(request.user)
            payers.save()

        for user in users:
            for other in users:
                debts = Debts.objects.filter(one=user, two=other) | Debts.objects.filter(one=other,two=other)
                if debts.exists():
                    print(debts[0].amount)

    return render(request, "purchase.html", {
        "group_name": group_name,
        "users": users,
    })

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"