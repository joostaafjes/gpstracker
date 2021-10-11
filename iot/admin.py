from django.contrib import admin

from .models import Message, GpsTrackerMessage


class MessageAdmin(admin.ModelAdmin):
    fields = ('method', 'body', 'parsed')
    readonly_fields = ('date',)
    list_display = ('method', 'body', 'parsed', 'date')

admin.site.register(Message, MessageAdmin)

class GpsTrackerMessageAdmin(admin.ModelAdmin):
    # fields = ('method', 'body', 'parsed')
    readonly_fields = ('date',)
    list_display = ('payload', 'latitude', 'longitude', 'alarm', 'battery', 'battery_perc', 'led_activity', 'movement_detection' , 'roll', 'pitch', 'altitude', 'hdop',  'get_received_date','date')

    @admin.display(ordering='message__date', description='Received date')
    def get_received_date(self, obj):
        return obj.message.date

admin.site.register(GpsTrackerMessage, GpsTrackerMessageAdmin)
