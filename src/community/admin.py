from django.contrib import admin
from .models import Channel, Topic, Reply
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    fields = ('name', 'order')


class TopicAdmin(SummernoteModelAdmin):
    list_display = ('title', 'channel', 'status', 'owner')
    fields = ('title', 'channel', 'topic_body')
    summernote_fields = ('topic_body')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TopicAdmin, self).save_model(request, obj, form, change)

admin.site.register(Topic, TopicAdmin)
