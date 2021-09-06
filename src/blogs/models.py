from django.contrib.auth.models import User
from django.db import models
from mdeditor.fields import MDTextField
from django.forms import ModelForm, TextInput, Textarea
from taggit.managers import TaggableManager
from .cntaggit import CnTaggedItem
from django.db.models.enums import IntegerChoices
from django.utils.translation import gettext as _


class Status(IntegerChoices):
    STATUS_DELETED = 0, _('删除')
    STATUS_NORMAL = 1, _('正常')
    STATUS_FROZEN = 2, _('冻结')
    

class Display(IntegerChoices):
    SHOW = 1, _('显示')
    HIDE = 0, _('隐藏')


class Category(models.Model):
    name = models.CharField(max_length=510, verbose_name=_("分类名称"))
    status = models.PositiveSmallIntegerField(default=Status.STATUS_NORMAL, choices=Status.choices, verbose_name=_("状态"))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("作者"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("创建时间"))

    class Meta:
        verbose_name = verbose_name_plural = _("分类")

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_menus(cls):
        categories = cls.objects.filter(status=Status.STATUS_NORMAL)
        return categories


class Archive(models.Model):
    year = models.CharField(verbose_name=_('年份'), max_length=10)

    class Meta:
        verbose_name = verbose_name_plural = _("年份")

    def __str__(self) -> str:
        return self.year


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="标题")
    summary = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    content = MDTextField(
        verbose_name="正文", help_text="请使用MarkDown格式", default="")
    status = models.PositiveSmallIntegerField(
        default=Status.STATUS_NORMAL, choices=Status.choices, verbose_name="状态")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="分类")
    tags = TaggableManager(through=CnTaggedItem)
    archive = models.ForeignKey(
        Archive, on_delete=models.CASCADE, null=True, verbose_name="存档", blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "博客"
        ordering = ['-id']

    def __str__(self) -> str:
        return self.title

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Status.STATUS_NORMAL).select_related('owner', 'category')

        return post_list, category

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=Status.STATUS_NORMAL)
        return queryset

    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(status=Status.STATUS_NORMAL).only('id', 'title').order_by('-pv')


class Comment(models.Model):
    target = models.ForeignKey(
        Post, verbose_name="评论目标", on_delete=models.CASCADE)
    content = models.CharField(max_length=2000, verbose_name="内容")
    status = models.PositiveSmallIntegerField(
        default=Status.STATUS_NORMAL, choices=Status.choices, verbose_name="状态")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "评论"

    @staticmethod
    def get_by_post(post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            post = None
            comment_list = []
        else:
            comment_list = post.comment_set.filter(status=Status.STATUS_NORMAL)

        return comment_list


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 5, }),
        }
