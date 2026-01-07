import asyncio
import sys
from pcpartpicker import API
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login
from app.forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
)


api = API()

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def root_view(request: HttpRequest) -> HttpResponse:
    return render(request, "root.html")

def sign_up_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect("landing")

    else:
        form = CustomUserCreationForm()

    return render(request, "sign_up.html", {"form": form})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("landing")

    else:
        form = CustomAuthenticationForm(request)

    return render(request, "login.html", {"form": form})

    
def landing_view(request):
    pass