from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from django.db import IntegrityError
from rest_framework import generics
from .models import Item
from .serializers import ItemSerializer


class ItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


def register(request):
    print(request,'收到了')
    if request.method != 'POST':
        return JsonResponse({'respMsg': '无效的请求方法', 'code': '999998'}, status=405)

    username = request.POST.get('username')
    password = request.POST.get('password')

    # 检验用户名是否存在
    if User.objects.filter(username=username).exists():
        return JsonResponse({'respMsg': '用户已存在', 'code': '999999'}, status=400)

    try:
        # 创建用户，使用set_password来确保密码安全
        user = User.objects.create_user(username=username)
        user.set_password(password)
        user.save()
        # 返回成功信息
        return JsonResponse({'respMsg': '用户创建成功', 'code': '000000'}, status=201)
    except IntegrityError as e:
        # 如果捕获到IntegrityError，说明可能是因为用户名已存在或其他唯一约束问题
        print('错误1',e)
        return JsonResponse({'respMsg': str(e), 'code': '999999'}, status=400)
    except Exception as e:
        # 其他异常处理
        print('错误2', e)
        return JsonResponse({'respMsg': str(e), 'code': '999999'}, status=500)