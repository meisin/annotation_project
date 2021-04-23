from django.contrib import admin

# Register your models here.
from .models import Sentences, Events, Event_arguments, Sent_validation, Event_validation


# Define the SentenceAdmin Class
class SentencesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sentences, SentencesAdmin)


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    pass



@admin.register(Event_arguments)
class Event_argumentsAdmin(admin.ModelAdmin):
    pass


@admin.register(Sent_validation)
class Sent_validationAdmin(admin.ModelAdmin):
    pass


@admin.register(Event_validation)
class Event_validationAdmin(admin.ModelAdmin):
    pass