import random
from app.models import *
from django.db.models import Q, Count
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login, update_session_auth_hash, logout, get_user_model
from app.forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
    UserUpdateForm,
)

User = get_user_model()

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
            login(request, form.get_user())
            return redirect("landing")
    else:
        form = CustomAuthenticationForm()
    return render(request, "login.html", {"form": form})


@login_required
def landing_view(request):
    all_computers = Computer.objects.all()
    random_computer = random.choice(all_computers) if all_computers else None

    user_computers = request.user.computers.all()  

    return render(request, "landing.html", {
        "random_computer": random_computer,
        "user_computers": user_computers,
    })

@login_required
def pc_list_view(request):
    user_computers = request.user.computers.all().order_by("name")

    query = request.GET.get("q", "").strip()
    if query:
        user_computers = user_computers.filter(name__icontains=query)

    paginator = Paginator(user_computers, 10)  # 10 computers per page
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "pc_list.html", {
        "page_obj": page_obj,
        "query": query,
    })

@login_required
def account_view(request):
    return render(request, "account.html")

@login_required
def social_view(request):
    filter_type = request.GET.get("filter", "popular")

    if request.method == "POST":
        subject = request.POST.get("subject")
        participants = request.POST.get("participants", "").split(",")

        conversation = Conversation.objects.create(subject=subject)
        conversation.participants.add(request.user)

        for username in participants:
            username = username.strip()
            if not username:
                continue
            try:
                user = User.objects.get(username=username)
                conversation.participants.add(user)
            except User.DoesNotExist:
                pass

        return redirect("chat-room", conversation_id=conversation.id)

    conversations = Conversation.objects.all()

    if filter_type == "mine":
        conversations = conversations.filter(
            participants=request.user
        ).distinct()

    else:  # popular
        conversations = conversations.annotate(
            num_participants=Count("participants")
        ).order_by("-num_participants")

    paginator = Paginator(conversations, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "social.html", {
        "page_obj": page_obj,
        "filter_type": filter_type,
    })


@login_required
def password_change_view(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            return redirect("landing")
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, "change.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def user_update_view(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("landing")
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, "update.html", {"form": form})

@login_required
def delete_view(request):
    if request.method != "POST":
        return redirect("root") 

    user = request.user
    logout(request)
    user.delete()
    return redirect("sign_up")

@login_required
def generic_part_list(request, pk, part_type):
    computer = get_object_or_404(Computer, pk=pk, owner=request.user)

    part_models = {
        "cpu": CPU,
        "gpu": GPU,
        "memory": Memory,
        "motherboard": Motherboard,
        "storagedrive": StorageDrive,
        "cpucooler": CPUCooler,
        "psu": PSU,
        "case": Case,
        "fan": CaseFans,
    }

    model_class = part_models.get(part_type)
    if not model_class:
        return redirect("builder", pk=pk)

    parts = model_class.objects.all().order_by("brand", "model")

    query = request.GET.get("q", "").strip()
    if query:
        parts = parts.filter(
            Q(brand__icontains=query) |
            Q(model__icontains=query)
        )

    paginator = Paginator(parts, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    field_names = [f.name for f in model_class._meta.get_fields() if not f.is_relation]

    return render(request, "part_list.html", {
        "computer": computer,
        "part_type": part_type,
        "page_obj": page_obj,
        "query": query,
        "field_names": field_names,  
    })


@login_required
def builder_view(request, pk):
    computer = get_object_or_404(Computer, pk=pk, owner=request.user)
    if request.method == "POST" and "name" in request.POST:
        computer.name = request.POST["name"]
        computer.save()
        return redirect("builder", pk=pk)
    return render(request, "builder.html", {"computer": computer})


@require_POST
@login_required
def create_computer(request):
    label = request.POST.get("label", "New Computer")
    computer = Computer.objects.create(owner=request.user, name=label)
    return redirect("builder", pk=computer.pk)

@login_required
def delete_computer(request, pk):
    computer = get_object_or_404(Computer, pk=pk, owner=request.user)

    if request.method == "POST":
        computer.delete()
        return redirect("pc-list")

    return redirect("pc-list")


@require_POST
@login_required
def add_part(request, pk, part_type, part_id):
    computer = get_object_or_404(Computer, pk=pk, owner=request.user)

    part_models = {
        "cpu": CPU,
        "gpu": GPU,
        "memory": Memory,
        "motherboard": Motherboard,
        "storagedrive": StorageDrive,
        "cpucooler": CPUCooler,
        "psu": PSU,
        "case": Case,
        "fan": CaseFans,
    }

    model = part_models.get(part_type)
    if not model:
        return redirect("builder", pk=pk)
    
    if request.POST.get("remove"):
        setattr(computer, part_type, None)
        computer.save()
        return redirect("builder", pk=pk)

    part = get_object_or_404(model, pk=part_id)
    setattr(computer, part_type, part)
    computer.save()

    return redirect("builder", pk=pk)

@login_required
def chat_room_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.order_by("timestamp").all()
    return render(request, "chat_room.html", {
        "conversation": conversation,
        "messages": messages,
        "user": request.user,
    })

@staff_member_required
@login_required
def admin_view(request):
    user_query = request.GET.get("user_q", "").strip()
    chat_query = request.GET.get("chat_q", "").strip()

    users = User.objects.all().order_by("username")
    if user_query:
        users = users.filter(username__icontains=user_query)
    user_paginator = Paginator(users, 10)
    user_page_number = request.GET.get("user_page") or 1
    user_page_obj = user_paginator.get_page(user_page_number)

    conversations = Conversation.objects.all().order_by("-created_at")
    if chat_query:
        conversations = conversations.filter(subject__icontains=chat_query)
    chat_paginator = Paginator(conversations, 10)
    chat_page_number = request.GET.get("chat_page") or 1
    chat_page_obj = chat_paginator.get_page(chat_page_number)

    return render(request, "admin.html", {
        "user_page_obj": user_page_obj,
        "chat_page_obj": chat_page_obj,
        "user_query": user_query,
        "chat_query": chat_query,
    })

@staff_member_required
@require_POST         
def admin_delete(request, pk):
    target = get_object_or_404(User, pk=pk)
    
    if target == request.user:
        return redirect("admin") 
        
    target.delete()
    return redirect("admin")

@staff_member_required
def admin_delete_conversation(request, pk):
    if request.method == "POST":
        conversation = get_object_or_404(Conversation, pk=pk)
        conversation.delete()
    return redirect("admin")