from django.contrib.auth.models import User
from django.db import models
from django.db.models.enums import IntegerChoices
from django_editorjs_fields import EditorJsJSONField, EditorJsTextField
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _


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


class Openess(models.TextChoices):
    PUBLIC = 'PUBLIC', _('Public')
    SEMI_PUBLIC = 'SEMI_PUBLIC', _('SemiPublic')
    PRIVATE = 'PRIVATE', _('Private')


class Level(models.IntegerChoices):
    LEVEL_A = 1, _('一级')
    LEVEL_B = 2, _('二级')
    LEVEL_C = 3, _('三级')
    LEVEL_D = 4, _('四级')
    LEVEL_E = 5, _('五级')

class Display(IntegerChoices):
    SHOW = 1, '显示'
    HIDE = 0, '隐藏'


class Word(models.Model):
    phrase = models.TextField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="作者")


class Story(models.Model):
    title = models.CharField(max_length=200, verbose_name="故事")
    desc = EditorJsTextField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="作者")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    history = HistoricalRecords()


class SpaceHub(models.Model):
    name = models.CharField(max_length=200, verbose_name="时空卡槽")
    content = EditorJsJSONField(verbose_name='描述')
    era = models.CharField(max_length=20)
    order = models.IntegerField("次序", blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    belong_to_story = models.ForeignKey(Story, on_delete=models.CASCADE, verbose_name="所属故事")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    history = HistoricalRecords()


class Stage(models.Model):
    title = models.CharField("标题", max_length=200)
    summary = models.CharField("摘要", max_length=1024, blank=True)
    content = EditorJsJSONField(verbose_name="内容")
    words_count = models.IntegerField("字数", default=0)
    type = models.PositiveSmallIntegerField("类型", default=StageType.TYPE_NONE, choices=StageType.choices)
    maturity = models.PositiveSmallIntegerField("成熟度", default=0)
    openess = models.CharField("开放性", max_length=20, choices=Openess.choices, default=Openess.PUBLIC)
    level = models.PositiveSmallIntegerField(
        "评级", choices=Level.choices, default=Level.LEVEL_A)
    status = models.PositiveSmallIntegerField("状态", default=Status.STATUS_NORMAL, choices=Status.choices)
    proofed = models.BooleanField('是否存证', default=False)
    coin = models.BigIntegerField('通证', default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    belong_to_story = models.ForeignKey(Story, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="所属故事")
    belong_to_hub = models.ForeignKey(SpaceHub, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="所属情节")
    pv = models.PositiveIntegerField("浏览量", default=1)
    uv = models.PositiveIntegerField("访问人数", default=1)
    history = HistoricalRecords()
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("修改时间", auto_now=True)
    digest = models.CharField("hash", max_length=128, default='', blank=True)

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
