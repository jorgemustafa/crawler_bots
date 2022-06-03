from django.contrib import admin
from steam.models import SkinData, SkinLog


@admin.register(SkinData)
class SkinDataAdmin(admin.ModelAdmin):
    list_display = ['weapon', 'gold', 'blue', 'urls']
    list_filter = ['weapon']


@admin.register(SkinLog)
class SkinLogAdmin(admin.ModelAdmin):
    list_display = ['weapon', 'gold', 'blue', 'urls']
    list_filter = ['weapon']
