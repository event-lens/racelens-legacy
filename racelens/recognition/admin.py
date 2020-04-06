from django.contrib import admin
from .models import Photo, Selfie, Event


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('imageId', 'event', 'user')


class SelfieAdmin(admin.ModelAdmin):
    list_display = ('user', 'id')


class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'slug', 'user')
    search_fields = ['event_name',]

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Selfie, SelfieAdmin)
admin.site.register(Event, EventAdmin)
