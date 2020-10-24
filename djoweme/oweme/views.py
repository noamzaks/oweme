from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


def home(request):
    return render(request, "home.html", {})

def purchase(request, group_name=None):
    return render(request, "purchase.html", {
        "group_name": group_name,
    })

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"