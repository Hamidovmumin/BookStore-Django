from django.contrib import admin
from . models import navbar

@admin.register(navbar)
class NavbarAdmin(admin.ModelAdmin):
    list_display = ('name','image','slug','id')
    prepopulated_fields = {'slug':('name',)}


