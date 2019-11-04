from django.contrib.auth.hashers import make_password
from django.db import models


# Create your models here.


class User(models.Model):
    # id 默认自动生成
    name = models.CharField(max_length=32, verbose_name='用户名')
    phone = models.CharField(max_length=11, unique=True)
    email = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    update_time = models.DateTimeField(auto_now=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    
    class Meta:
        db_table = 'user'
    
    def set_password(self, pwd):
        self.password = make_password(pwd)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'icon': self.icon,
            'update_time': self.update_time.strftime('%Y.%m.%d %H:%M'),
            'add_time': self.add_time.strftime('%Y.%m.%d %H:%M')
        }


class UserInfo(models.Model):
    sex = models.IntegerField(default=2)  # 0 代表女性 1 代表 男性 2 代表 保密
    website = models.CharField(max_length=64, verbose_name='个人网站')
    git = models.CharField(max_length=64, verbose_name='git地址')
    wechat = models.CharField(max_length=255, verbose_name='微信二维码图片地址')
    desc = models.CharField(max_length=1024, verbose_name='个人简介')
    address = models.CharField(max_length=100, default='', verbose_name='工作地址')
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE, related_name='info')
    update_time = models.DateTimeField(auto_now=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    
    class Meta:
        db_table = 'user_info'


class Comment(models.Model):
    """一级评论"""
    tweet = models.ForeignKey('tweet.Tweet', on_delete=models.CASCADE, related_name='comments')
    be_from = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=1024)
    update_time = models.DateTimeField(auto_now=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    
    class Meta:
        db_table = 'comment'
    
    def to_dict(self):
        return {
            'id': self.id,
            'be_from': self.be_from.name,
            'content': self.content,
            'update_time': self.update_time.strftime('%Y.%m.%d %H:%M'),
            'add_time': self.add_time.strftime('%Y.%m.%d %H:%M'),
            'is_author': 1 if self.be_from_id == self.tweet.user_id else 0,
            'second_comment': [i.to_dict() for i in self.second_comments.all()]
        }


class SecondComment(models.Model):
    """二级评论"""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='second_comments')
    content = models.CharField(max_length=1024)
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second_comments_to')
    be_from = models.ForeignKey(User, related_name='second_comments_from', on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    
    class Meta:
        db_table = 'second_comment'
    
    def to_dict(self):
        return {
            'id': self.id,
            'be_from': self.be_from.name,
            'to': self.to.name,
            'content': self.content,
            'is_author': 1 if self.be_from_id == self.comment.tweet.user_id else 0,
            'update_time': self.update_time.strftime('%Y.%m.%d %H:%M'),
            'add_time': self.add_time.strftime('%Y.%m.%d %H:%M')
        }
