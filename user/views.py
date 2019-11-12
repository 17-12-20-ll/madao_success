from django.http import JsonResponse, HttpResponse

from django.views.decorators.csrf import csrf_exempt

from user.models import User
from utils.gen_captcha import get_captcha
from utils.gen_token import create_token, get_data_obj, check_token, get_token_obj
from utils.sms_code_helper import send_sms_code_v2


def captcha(request):
    if request.method == 'GET':
        # 获取当当前时间戳的值
        _time = request.GET.get('time')
        result = get_captcha()
        text = result['text']
        img = result['img']
        res = HttpResponse(img, 'image/png')
        # max_age:代表从请求时间开始计算，expires代表过期时间，从获取到开始计算，关系：max-age = expires- request_time
        res.set_cookie('code', text, 60)
        # 不重要的信息放在cookie中,好处是，cookie自带过期时间
        return res


def phone_send_code(request):
    if request.method == 'GET':
        phone = request.GET.get('phone')
        # 发送手机验证码,将成功后的msg_id保存到浏览器中
        # msg_id = send_sms_code(phone)
        code = send_sms_code_v2(phone)
        obj = get_data_obj(phone=phone, code=code, type='send_code')
        # 创建token
        token = create_token(obj)
        # 使用非对称加密，对数据进行加密
        # data = encrypt({'msg_id': msg_id, 'phone': phone})
        return JsonResponse({'code': 200, 'msg': '发送成功', 'token': token})


def check_is_register(request):
    if request.method == 'GET':
        phone = request.GET.get('phone')
        # 判断当前用户是否注册
        isU = User.objects.filter(phone=phone).first()
        if isU:
            return JsonResponse({'code': 101, 'msg': '当前手机号已被注册'})
        else:
            return JsonResponse({'code': 200, 'msg': 'success'})


@csrf_exempt
def phone_register(request):
    """使用手机号注册"""
    if request.method == 'POST':
        phone = request.POST.get('phone')
        # 校验手机号如果被注册，则不进行注册
        if User.objects.filter(phone=phone):
            return JsonResponse({'code': 101, 'msg': '当前手机号已被注册'})
        name = request.POST.get('name')
        # data = request.POST.get('data')
        sms_token = request.POST.get('token')
        code = request.POST.get('code')
        pwd = request.POST.get('pwd')
        # 解析data
        # obj = decrypt(data)  # {'msg_id': msg_id, 'phone': phone}
        if check_token(sms_token):
            obj = get_token_obj(sms_token)
            if obj['phone'] != phone:
                return JsonResponse({'code': 100, 'msg': '注册手机号与发送验证码手机号不一致！'})
            if obj['code'] != code:
                return JsonResponse({'code': 50010, 'msg': '验证码错误'})
            u = User()
            u.phone = phone
            u.set_password(pwd)
            u.name = name
            u.save()
            user_info_obj = get_data_obj(id=u.id, type='login_info')
            token = create_token(user_info_obj)
        else:
            return JsonResponse({'code': 50011, 'msg': '验证码过期'})
        return JsonResponse({'code': 200, 'msg': '注册成功', 'token': token})


# 手机号、密码登陆
@csrf_exempt
def login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        pwd = request.POST.get('pwd')
        u = User.objects.filter(phone=phone).first()
        if u.verify_password(pwd):
            user_info_obj = get_data_obj(id=u.id, type='login_info')
            token = create_token(user_info_obj)
            return JsonResponse({'code': 200, 'msg': 'success', 'token': token})
        else:
            return JsonResponse({'code': 100, 'msg': '密码错误'})
