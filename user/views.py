import json

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from rest_framework import generics
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

from image.models import ImageSave
from user.models import UserProfile


def register(request):
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
        profile = UserProfile.objects.get(user=resUser)
        if resUser and resUser.is_active:
            auth.login(request, resUser)
            return JsonResponse({'message': '用户登录成功', 'data': {
                'id': resUser.id,
                'userName': resUser.username,
                'firstName': resUser.first_name,
                'lastName': resUser.last_name,
                'avatarUrl': profile.avatar.image.url if profile.avatar else '',
                'avatarId': profile.avatar.id if profile.avatar else '',
            }, 'ok': True, 'code': '200'}, status=200)
        else:
            return JsonResponse({'message': '登录失败，用户名或密码错误', 'code': '400'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'message': '请求数据格式错误', 'code': '400'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e), 'code': '500'}, status=500)


def getUserInfo(request):
    if request.method != 'GET':
        return JsonResponse({'message': '无效的请求方法', 'code': '999998'}, status=405)
    try:
        id = request.GET.get('id')
        if not id:
            return JsonResponse({'message': '缺少用户ID', 'code': '400'}, status=400)
        # 尝试获取 UserProfile 对象
        try:
            profile = UserProfile.objects.get(user__id=id)
        except User.DoesNotExist:
            return JsonResponse({'message': '用户信息不存在', 'code': '400'}, status=400)
        # 检查用户是否活跃
        if profile.user.is_active:
            return JsonResponse({'message': '获取信息成功', 'data': {
                'id': profile.user.id,
                'userName': profile.user.username,
                'firstName': profile.user.first_name,
                'lastName': profile.user.last_name,
                'avatarUrl': profile.avatar.image.url if profile.avatar else '',
                'avatarId': profile.avatar.id if profile.avatar else '',
            }, 'ok': True, 'code': '200'}, status=200)
        else:
            return JsonResponse({'message': '用户账户未激活', 'code': '400'}, status=400)

    except Exception as e:
        return JsonResponse({'message': str(e), 'code': '500'}, status=500)


def update_user_info(request):
    if request.method != 'POST':
        return JsonResponse({'message': '无效的请求方法', 'code': '999998'}, status=405)
    try:
        data = json.loads(request.body)
        user_id = data.get('id')
        if not user_id:
            return JsonResponse({'message': '用户ID未提供', 'code': '400'}, status=400)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'message': '用户不存在', 'code': '400'}, status=400)

        # 更新用户信息
        user.username = data.get('userName', user.username)
        user.password = data.get('password', user.password)
        user.first_name = data.get('firstName', user.first_name)
        user.last_name = data.get('lastName', user.last_name)
        profile, created = UserProfile.objects.get_or_create(user=user)
        image_id = data.get('avatarId')
        if image_id:
            try:
                image = ImageSave.objects.get(id=image_id)
                profile.avatar = image

            except ImageSave.DoesNotExist:
                return JsonResponse({'message': '图片不存在', 'code': '400'}, status=400)
        # 保存更新后的信息
        user.save()
        profile.save()  # 确保保存UserProfile实例
        return JsonResponse({
            'message': '用户信息更新成功',
            'data': {
                'id': user.id,
                'userName': user.username,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'avatarId': profile.avatar.id if profile.avatar else None,
            },
            'ok': True,
            'code': '200'
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'message': '请求数据格式错误', 'code': '400'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e), 'code': '500'}, status=500)
