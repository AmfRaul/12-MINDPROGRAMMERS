from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "tipo_conta", "telefone", "is_staff", "is_active"]
    list_filter = ["tipo_conta", "is_staff", "is_active"]
    search_fields = ["username", "email", "telefone"]

    fieldsets = UserAdmin.fieldsets + (
        ("Dados da FieldReach", {"fields": ("tipo_conta", "telefone")}),
    )
