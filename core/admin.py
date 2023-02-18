from django.contrib import admin
from core.models import *

@admin.register(Tier)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
