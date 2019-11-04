from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from tweet.models import Tweet
from user.models import Comment, SecondComment
from utils.gen_num import gen_random_num


@csrf_exempt
def add_tweet(request):
    """添加推文"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        user_id = request.POST.get('user_id')
        t = Tweet()
        t.title = title
        t.content = content
        t.user_id = user_id
        t.read_num = gen_random_num()
        t.save()
        return JsonResponse({'code': 200, 'msg': 'success'})


def get_tweet(request):
    if request.method == 'GET':
        tweet_id = request.GET.get('id')
        t = Tweet.objects.filter(id=tweet_id).first()
        return JsonResponse({'code': 200, 'msg': 'success', 'data': t.to_full_dict()})


@csrf_exempt
def add_comment(request):
    """添加评论"""
    if request.method == 'POST':
        tweet_id = request.POST.get('tweet_id')
        be_from_id = request.POST.get('be_from_id')
        content = request.POST.get('content')
        c = Comment()
        c.tweet_id = tweet_id
        c.be_from_id = be_from_id
        c.content = content
        c.save()
        return JsonResponse({'code': 200, 'msg': 'success'})


@csrf_exempt
def add_second_comment(request):
    """添加二级评论"""
    if request.method == 'POST':
        sc = SecondComment()
        sc.be_from_id = request.POST.get('be_from_id')
        sc.to_id = request.POST.get('to_id')
        sc.content = request.POST.get('content')
        sc.comment_id = request.POST.get('comment_id')
        sc.save()
        return JsonResponse({'code': 200, 'msg': 'success'})
