from django.contrib import admin

from tasks.models import ForestChangeTask



@admin.register(ForestChangeTask)
class ForestChangeTaskAdmin(admin.ModelAdmin):
    list_display = ['uid', 'datetime_created', 'region', 'gain_area', 'loss_area', 'total_area', 'status']
    search_fields = []
    list_filter = []
    ordering = ['-datetime_created']
    readonly_fields = ['datetime_updated']

