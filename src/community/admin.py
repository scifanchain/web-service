from django.contrib import admin
from .models import Channel, Topic, Reply
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    fields = ('name', 'order')


@admin.register(Topic)
class TopicAdmin(SummernoteModelAdmin):
    list_display = ('title', 'channel', 'status', 'owner')
    fields = ('title', 'channel', 'topic_body', 'owner')
    summernote_fields = ('topic_body')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TopicAdmin, self).save_model(request, obj, form, change)


@admin.register(Reply)
class ReplyAdmin(SummernoteModelAdmin):
    list_display = ('reply_body', 'owner')
    fields = ('reply_body','target')
    summernote_fields = ('reply_body')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(ReplyAdmin, self).save_model(request, obj, form, change)
