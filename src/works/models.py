from django.contrib.auth.models import User
from django.db import models
from django.db.models.enums import IntegerChoices
from django_editorjs_fields import EditorJsJSONField, EditorJsTextField
from simple_history.models import HistoricalRecords


class Status(IntegerChoices):
    STATUS_DELETED = 0, '删除'
    STATUS_NORMAL = 1, '正常'
    STATUS_FROZEN = 2, '冻结'


class StageType(IntegerChoices):
    TYPE_NONE = 0, '未定义'
    TYPE_ERA = 1, '时间'
    TYPE_PLACE = 2, '地点'
    TYPE_PERSON = 3, '人物'
    TYPE_EVENT = 4, '事件'
    TYPE_CONCEPT = 5, '概念'


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


class Plot(models.Model):
    name = models.CharField(max_length=200, verbose_name="故事章节")
    content = EditorJsJSONField(verbose_name='情节内容')
    order = models.IntegerField("次序", blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    belong_to_story = models.ForeignKey(Story, on_delete=models.CASCADE, verbose_name="所属故事")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    history = HistoricalRecords()


class Stage(models.Model):
    title = models.CharField("标题", max_length=200)
    summary = models.CharField("摘要", max_length=1024, blank=True)
    content = EditorJsJSONField(verbose_name='内容')
    type = models.PositiveSmallIntegerField("类型", default=StageType.TYPE_NONE, choices=StageType.choices)
    status = models.PositiveSmallIntegerField("状态", default=Status.STATUS_NORMAL, choices=Status.choices)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    belong_to_story = models.ForeignKey(Story, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="所属故事")
    belong_to_plot = models.ForeignKey(Plot, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="所属情节")
    pv = models.PositiveIntegerField("浏览量", default=1)
    uv = models.PositiveIntegerField("访问人数", default=1)
    history = HistoricalRecords()
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("修改时间", auto_now=True)

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
