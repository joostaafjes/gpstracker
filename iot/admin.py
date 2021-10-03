from django.contrib import admin

from .models import Message


class MessageAdmin(admin.ModelAdmin):
    fields = ('method', 'body', 'parsed')
    readonly_fields = ('date',)
    list_display = ('method', 'body', 'parsed', 'date')

admin.site.register(Message, MessageAdmin)