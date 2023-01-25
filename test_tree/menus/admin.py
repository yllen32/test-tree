from django.contrib import admin

from .models import Field, Menu, FieldRelations

@admin.register(Field, Menu, FieldRelations)
class MenuAdmin(admin.ModelAdmin):
    pass
