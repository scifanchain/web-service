from django.db import models
from django.db.models.enums import IntegerChoices
from django.contrib.auth.models import User


class TopicCategory(models.Model):
    name = models.CharField(max_length=20, verbose_name="分类名称")
    order = models.IntegerField()


# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    post = models.CharField(max_length=200, verbose_name="内容")
    category = models.ForeignKey(TopicCategory, on_delete=models.CASCADE, verbose_name="分类")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="修改时间")
