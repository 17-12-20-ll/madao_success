from django.db import models

# Create your models here.
from tweet.models import Tweet


# 栏目 自关联
class Column(models.Model):
    name = models.CharField(max_length=32, unique=True, null=False)
    desc = models.CharField(max_length=255, null=True, verbose_name='栏目描述')
    column = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None, related_name='columns',
                               verbose_name='栏目父节点')
    update_time = models.DateTimeField(auto_now=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    
    class Meta:
        db_table = 'column'


# 栏目与文章多对多
class MidColumnTweet(models.Model):
    c = models.ForeignKey(Column, on_delete=models.CASCADE)
    t = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'mid_column_tweet'
