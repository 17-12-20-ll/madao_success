import itsdangerous as itsdangerous
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from user.models import User


@csrf_exempt
def phone_login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        pwd = request.POST.get('pwd')
        u = User.objects.filter(phone=phone).first()
        if u:
            u.set_password(phone[5:])
            if check_password(pwd, u.password):
                return JsonResponse({'code': 200, 'msg': 'success'})
        else:
            u = User()
            u.phone = phone
            u.set_password(pwd)
            u.save()
            return JsonResponse({'code': 200, 'msg': 'success'})

