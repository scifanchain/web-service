from django.contrib.auth.models import User
from django.db import models
from django.db.models.enums import IntegerChoices
from django_editorjs_fields import EditorJsJSONField, EditorJsTextField
from simple_history.models import HistoricalRecords


class Status(IntegerChoices):
    STATUS_DELETED = 0, '删除'
    STATUS_NORMAL = 1, '正常'
    STATUS_FROZEN = 2, '冻结'


class StageKind(IntegerChoices):
    KIND_NONE = 0, '未定义'
    KIND_ERA = 1, '时间'
    KIND_PLACE = 2, '地点'
    KIND_PERSON = 3, '人物'
    KIND_EVENT = 4, '事件'
    KIND_CONCEPT = 5, '概念'


class Display(IntegerChoices):
    SHOW = 1, '显示'
    HIDE = 0, '隐藏'


class Story(models.Model):
    title = models.CharField(max_length=200, verbose_name="故事")
    desc = EditorJsTextField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="作者")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    history = HistoricalRecords()


class Chapter(models.Model):
    name = models.CharField(max_length=200, verbose_name="故事章节")
    order = models.IntegerField()
    history = HistoricalRecords()
    belong_to_story = models.IntegerField(blank=True, default=0, verbose_name="所属故事")


class Stage(models.Model):
    title = models.CharField(max_length=200, verbose_name="标题")
    summary = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    content = EditorJsJSONField()
    kind = models.PositiveSmallIntegerField(default=StageKind.KIND_NONE, choices=StageKind.choices, verbose_name="类型")
    status = models.PositiveSmallIntegerField(default=Status.STATUS_NORMAL, choices=Status.choices, verbose_name="状态")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    belong_to_story = models.IntegerField(blank=True, default=0, verbose_name="所属故事")
    belong_to_chapter = models.IntegerField(blank=True, default=0, verbose_name="所属章节")
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)
    history = HistoricalRecords()
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        verbose_name = verbose_name_plural = "作品"
        ordering = ['-id']

    def __str__(self) -> str:
        return self.title

    @classmethod
    def latest_stages(cls):
        queryset = cls.objects.filter(status=Status.STATUS_NORMAL)
        return queryset

    @classmethod
    def hot_stages(cls):
        return cls.objects.filter(status=Status.STATUS_NORMAL).only('id', 'title').order_by('-pv')
