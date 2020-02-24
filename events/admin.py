from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	list_display = ('user', 'target', 'created', 'verb')
	list_filter = ('created', )
	search_fields = ('verb', )