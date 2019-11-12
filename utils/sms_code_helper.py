import random
import time

from madao.settings import APP_KEY, MASTER_SECRET
from utils import jsms

sms_client = jsms.Jsms(APP_KEY, MASTER_SECRET)


def send_sms_code(phone, tmp_id='1'):
    # 验证码过期时间由极光短信网站设置，默认5分钟
    result = sms_client.send_code(phone, tmp_id)
    return result['msg_id']


def check_sms_code(msg_id, code):
    # {'is_valid': False, 'error': {'code': 50012, 'message': 'verified code'}}
    # {'is_valid': False, 'error': {'code': 50010, 'message': 'invalid code'}}
    # {'is_valid': True}
    return sms_client.verify_code(msg_id, code)


def random_code():
    nums = [str(random.randint(0, 9)) for _ in range(6)]
    return ''.join(nums)


# 使用通知短信进行验证码发送，自定义控制验证码的使用时长
def send_sms_code_v2(phone):
    code = random_code()
    result = sms_client.send_teml(phone, '172117', temp_para={'code': code})
    return code


if __name__ == '__main__':
    # print(send_sms_code_v2('13111856135'))
    pass
    # print(sms_client.send_code('13111856135', '1'))
    
    # print(sms_client.verify_code('885580595545', '651387'))
