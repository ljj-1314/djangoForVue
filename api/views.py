import json

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
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
    print(request, '收到了', request.body, request.POST)
    if request.method != 'POST':
        return JsonResponse({'message': '无效的请求方法', 'code': '405'}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('passWord')
        email = data.get('email')
        # 检验用户名是否存在
        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': '用户已存在', 'code': '400'}, status=400)

        # 创建用户，使用set_password来确保密码安全
        user = User.objects.create_user(username=username, password=password, email=email)
        user.set_password(password)
        user.save()
        return JsonResponse({'message': '用户创建成功', 'ok': True, 'code': '200'}, status=200)
    except json.JSONDecodeError as e:
        return JsonResponse({'message': '请求数据格式错误', 'code': '400'}, status=400)
    except IntegrityError as e:
        print('错误1', e)
        return JsonResponse({'message': str(e), 'code': '400'}, status=400)
    except Exception as e:
        print('错误2', e)
        return JsonResponse({'message': str(e), 'code': '500'}, status=500)


def login(request):
    if request.method != 'POST':
        return JsonResponse({'message': '无效的请求方法', 'code': '999998'}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('passWord')
        resUser = auth.authenticate(request, username=username, password=password)

        if resUser and resUser.is_active:
            auth.login(request, resUser)
            return JsonResponse({'message': '用户登录成功', 'ok': True, 'code': '200'}, status=200)
        else:
            return JsonResponse({'message': '登录失败，用户名或密码错误', 'code': '400'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'message': '请求数据格式错误', 'code': '400'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e), 'code': '500'}, status=500)
