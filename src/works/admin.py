from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Story, SpaceHub, Stage, Word


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('phrase', 'owner')


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'owner')
    fields = ('title', 'desc')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(StoryAdmin, self).save_model(request, obj, form, change)


@admin.register(SpaceHub)
class SpaceHubAdmin(admin.ModelAdmin):
    list_display = ('name', 'belong_to_story')
    fields = ('name', 'order', 'belong_to_story')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SpaceHubAdmin, self).save_model(request, obj, form, change)


@admin.register(Stage)
class StageAdmin(SimpleHistoryAdmin):
    list_display = ('title', 'type', 'owner', 'created')
    fields = ('title', 'summary', 'content','maturity', 'openess')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(StageAdmin, self).save_model(request, obj, form, change)
