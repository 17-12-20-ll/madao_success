import hashlib
import time

from django.core import signing
from django.core.cache import cache

from madao.settings import CODE_TIME_OUT, LOGIN_TIME_OUT, LOGIN_ADMIN_TIME_OUT, CODE_TIME_OUT_TEST

KEY = 'LiLong'
SALT = '1096195574@qq.com'
HEADER = {'typ': 'JWP', 'alg': 'default'}


def get_data_obj(**kwargs):
    """传递参数规则：传递任意参数，但必须传一个m_type字段，代表当前是发送验证、注册、订单支付等"""
    """
    type:
    send_code:代表保存验证码时的缓存,
    login_info:代表保存登陆用户的信息,
    img_code:代表保存图形验证码的信息,
    admin_info:代表保存登录的管理员的信息
    iat:
    代表保存token时的时间戳
    """
    kwargs['iat'] = time.time()
    return kwargs


def encrypt(obj):
    """加密"""
    # salt给生成的签名加盐，进行解码的时候使用
    value = signing.dumps(obj, key=KEY, salt=SALT)
    value = signing.b64_encode(value.encode()).decode()
    return value


def decrypt(src):
    """解密"""
    src = signing.b64_decode(src.encode()).decode()
    raw = signing.loads(src, key=KEY, salt=SALT)
    return raw


def create_token(obj):
    """生成token信息保存到缓存中，并返回token"""
    # 1. 加密头信息
    header = encrypt(HEADER)
    # 2. 构造Payload
    payload = obj
    payload = encrypt(payload)
    # 3. 生成签名
    md5 = hashlib.md5()
    md5.update(("%s.%s" % (header, payload)).encode())
    signature = md5.hexdigest()
    token = "%s.%s.%s" % (header, payload, signature)
    # 存储到缓存中
    if obj['type'] == 'send_code':
        cache.set(obj['phone'] + '_' + obj['type'], token, CODE_TIME_OUT_TEST)
    if obj['type'] == 'login_info':
        cache.set(str(obj['id']) + '_' + obj['type'], token, LOGIN_TIME_OUT)
    if obj['type'] == 'img_code':
        cache.set(obj['time'] + obj['only_num'], token, CODE_TIME_OUT)
    if obj['type'] == 'admin_info':
        cache.set(str(obj['id']) + '_' + obj['type'], token, LOGIN_ADMIN_TIME_OUT)
    return token


def get_payload(token):
    """获取负载数据"""
    payload = str(token).split('.')[1]
    payload = decrypt(payload)
    return payload


def get_token_obj(token):
    """获取token转化后的数据"""
    payload = get_payload(token)
    return payload


def check_token(token):
    """检查当前token是否可用"""
    obj = get_token_obj(token)
    last_token = ''
    if obj['type'] == 'send_code':
        last_token = cache.get(obj['phone'] + '_' + obj['type'])
    if obj['type'] == 'login_info':
        last_token = cache.get(str(obj['id']) + '_' + obj['type'])
    if obj['type'] == 'img_code':
        last_token = cache.get(obj['time'] + obj['only_num'])
    if obj['type'] == 'admin_info':
        last_token = cache.get(str(obj['id']) + '_' + obj['type'])
    # 当redis中的数据过期时，获取没有该数据信息时，就会返回None
    if last_token:
        return True
    return False


def del_cache(key):
    """删除缓存--清除redis数据"""
    cache.delete(key)
