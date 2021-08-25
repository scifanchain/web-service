from django.contrib import admin
from .models import Story, Chapter, Stage


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'owner')
    fields = ('title', 'desc')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(StoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'belong_to_story')
    fields = ('name', 'order', 'belong_to_story')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(ChapterAdmin, self).save_model(request, obj, form, change)


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'owner', 'created')
    fields = ('title', 'summary', 'content')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(StageAdmin, self).save_model(request, obj, form, change)
