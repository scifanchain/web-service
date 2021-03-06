from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .adminforms import PostAdminForm
from .models import Post, Category, Comment, Archive
import datetime
from django.db.models import F


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

class ArchiveAdmin(admin.ModelAdmin):
    list_display = ('time', 'count')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'category', 'owner', 'status', 'created', 'operator', 'tag_list')
    list_display_links = []
    search_fields = ['title', 'category__name']
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True
    fields = (
        'title',
        'summary',
        'category',
        'thumb',
        'thumb_width',
        'thumb_height',
        'content',
        'status',
        'tags',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blogs_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'
    tag_list.short_descriptions = 'tags'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        # 按年份存档及数量
        try:
            t = Archive.objects.get(
                time=str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().strftime('%m')))
            t.count = F('count') + 1
        except:
            t = Archive(time=str(datetime.datetime.now().year) +
                        "-" + str(datetime.datetime.now().strftime('%m')))
        t.save()

        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'content', 'created')
