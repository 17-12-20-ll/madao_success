from django.db import models

# Create your models here.
from user.models import User


class Tweet(models.Model):
    """support 后续考虑，分词检索"""
    # id 默认自动生成
    title = models.CharField(max_length=32, unique=True, null=False)
    content = models.CharField(max_length=10240)  # 长度未知
    user = models.ForeignKey(User, related_name='tweets', on_delete=models.CASCADE)
    read_num = models.IntegerField()
    update_time = models.DateTimeField(auto_now=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    
    class Meta:
        db_table = 'tweet'
    
    def to_full_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user': self.user.name,
            'read_num': self.read_num,
            'update_time': self.update_time.strftime('%Y.%m.%d %H:%M'),
            'add_time': self.add_time.strftime('%Y.%m.%d %H:%M'),
            'comments': [i.to_dict() for i in self.comments.all()]
        }
