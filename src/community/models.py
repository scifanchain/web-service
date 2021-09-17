from django.db import models
from django.db.models.enums import IntegerChoices
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class Status(IntegerChoices):
    STATUS_DELETED = 0, _('删除')
    STATUS_NORMAL = 1, _('正常')
    STATUS_FROZEN = 2, _('冻结')


class Display(IntegerChoices):
    SHOW = 1, _('显示')
    HIDE = 0, _('隐藏')


class Channel(models.Model):
    name = models.CharField(max_length=20, verbose_name="频道名称")
    order = models.IntegerField()

    def __str__(self) -> str:
        return self.name


# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    topic_body = models.TextField(verbose_name="内容")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, verbose_name="分类", default='')
    status = models.PositiveSmallIntegerField(
        default=Status.STATUS_NORMAL, choices=Status.choices, verbose_name=_("状态"))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    top = models.BooleanField(blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="修改时间")


class Reply(models.Model):
    target = models.ForeignKey(
        Topic, verbose_name=_("回复主题"), on_delete=models.CASCADE)
    reply_body = models.CharField(max_length=500, verbose_name=_("内容"))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("作者"))
    status = models.PositiveSmallIntegerField(
        default=Status.STATUS_NORMAL, choices=Status.choices, verbose_name=_("状态"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("创建时间"))

    class Meta:
        verbose_name = verbose_name_plural = _("回复")
