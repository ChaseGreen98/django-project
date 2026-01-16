"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path("admin/", admin_view, name="admin"),
    path("admin/delete/<int:pk>/", admin_delete, name="admin-delete"),
    path("", root_view, name="root"),
    path("sign-up/", sign_up_view, name="sign_up"),
    path("login/", login_view, name="login"),
    path("landing/", landing_view, name="landing"),
    path("account/", account_view, name="account"),
    path("social/", social_view, name="social"),
    path("password-change/", password_change_view, name="change"),
    path("account/delete/", delete_view, name="account-delete"),
    path("logout/", logout_view, name="logout"),
    path("user-update/", user_update_view, name="update"),
    path("chat/<int:conversation_id>/", chat_room_view, name="chat-room"),
    path("builder/<int:pk>/", builder_view, name="builder"),
    path("pc-list/", pc_list_view, name="pc_list"),
    path("computer/delete/<int:pk>", delete_computer, name="delete_computer"),
    path("builder/create/", create_computer, name="create_computer"),
    path(
        "builder/<int:pk>/<str:part_type>/",
        generic_part_list,
        name="part_list"
    ),
    path(
        "builder/<int:pk>/add/<str:part_type>/<int:part_id>/",
        add_part,
        name="add_part"
    ),
]