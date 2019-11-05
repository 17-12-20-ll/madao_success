from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from common.models import Column


@csrf_exempt
def add_column(request):
    """添加栏目"""
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        code = request.POST.get('code')
        column_id = request.POST.get('column_id', '')
        c = Column()
        c.name = name
        c.desc = desc
        c.code = code
        # 没有传入父栏目时，代表该栏目是一级栏目
        c.column_id = column_id if column_id else None
        c.save()
        return JsonResponse({'code': 200, 'msg': 'success'})


def get_column_all(request):
    if request.method == 'GET':
        c = Column.objects.all()
        return JsonResponse({'code': 200, 'msg': 'success', 'data': [i.to_dict() for i in c]})


def get_one_column(request):
    if request.method == 'GET':
        c_one = Column.objects.filter(column_id=None)
        return JsonResponse({'code': 200, 'msg': 'success', 'data': [i.to_dict() for i in c_one]})
