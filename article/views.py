import json

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import F
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from article.models import UserArticle


# Create your views here.
def create(request):
    if request.method != 'POST':
        return JsonResponse({'message': '无效的请求方法', 'code': '405'}, status=405)

    try:
        data = json.loads(request.body)
        title = data.get('title')
        content = data.get('content')
        user_id = data.get('user_id')

        if not title:
            return JsonResponse({'message': '标题不能为空', 'code': '400'}, status=400)
        if not user_id:
            return JsonResponse({'message': '用户ID不能为空', 'code': '400'}, status=400)
        try:
            user = User.objects.get(id=user_id)
            print(user, '用户信息')
        except ObjectDoesNotExist:
            return JsonResponse({'message': '用户不存在', 'code': '400'}, status=400)

        if not user.is_active:
            return JsonResponse({'message': '用户未激活', 'code': '400'}, status=400)

            # 创建并保存文章
        article = UserArticle(
            title=title,
            content=content,
            author=user,  # 设置作者为获取到的用户对象
        )
        article.save()

        return JsonResponse({'message': '文章创建成功', 'data': {'no': article.no}, 'code': '200'}, status=200)
    except json.JSONDecodeError as e:
        return JsonResponse({'message': '请求数据格式错误', 'code': '400'}, status=400)
    except IntegrityError as e:
        print('错误1', e)
        return JsonResponse({'message': str(e), 'code': '400'}, status=400)
    except Exception as e:
        print('错误2', e)
        return JsonResponse({'message': str(e), 'code': '500'}, status=500)


def update(request):
    if request.method != 'POST':
        return JsonResponse({'message': '无效的请求方法', 'code': '405'}, status=405)

    try:
        data = json.loads(request.body)
        no = data.get('no')
        title = data.get('title')
        content = data.get('content')
        user_id = data.get('user_id')

        if not title:
            return JsonResponse({'message': '标题不能为空', 'code': '400'}, status=400)
        if not user_id:
            return JsonResponse({'message': '用户ID不能为空', 'code': '400'}, status=400)
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return JsonResponse({'message': '用户不存在', 'code': '400'}, status=400)

        if not user.is_active:
            return JsonResponse({'message': '用户未激活', 'code': '400'}, status=400)
        try:
            article = UserArticle.objects.get(no=no)
        except ObjectDoesNotExist:
            return JsonResponse({'message': '不存在该文章，请重试', 'code': '400'}, status=400)

            # 创建并保存文章
        article_updated = UserArticle.objects.filter(no=no, author=user).update(
            title=title,
            content=content,
            updateTime=timezone.now()  # 如果需要更新更新时间
        )

        if article_updated == 1:
            return JsonResponse({'message': '文章编辑成功', 'data': {'no': no}, 'code': '200'}, status=200)
        else:
            return JsonResponse({'message': '文章更新失败', 'code': '400'}, status=400)
    except json.JSONDecodeError as e:
        return JsonResponse({'message': '请求数据格式错误', 'code': '400'}, status=400)
    except IntegrityError as e:
        print('错误1', e)
        return JsonResponse({'message': str(e), 'code': '400'}, status=400)
    except Exception as e:
        print('错误2', e)
        return JsonResponse({'message': str(e), 'code': '500'}, status=500)


def getPagedList(request):
    if request.method != 'GET':
        return JsonResponse({'message': '无效的请求方法', 'code': '405'}, status=405)

    pageIndex = request.GET.get('pageIndex')
    pageSize = request.GET.get('pageSize')
    authorName = request.GET.get('authorName')
    createTime = request.GET.get('createTime')
    updateTime = request.GET.get('UpdateTime')

    if not pageSize or not pageIndex:
        return JsonResponse({'message': '分页数和页码不能为空', 'code': '405'}, status=405)

    # 默认返回所有文章
    articles = UserArticle.objects.all()

    # 过滤作者姓名
    if authorName:
        users = User.objects.annotate(
            full_name=Concat(F('first_name'), F('last_name'))
        ).filter(full_name__icontains=authorName)
        articles = articles.filter(author__in=users)

    # 过滤创建时间范围
    if createTime:
        create_time_range = json.loads(createTime)  # 解析为列表
        articles = articles.filter(createTime__range=create_time_range)

    # 过滤更新时间范围
    if updateTime:
        update_time_range = json.loads(updateTime)  # 解析为列表
        articles = articles.filter(updateTime__range=update_time_range)

    # 分页处理
    paginator = Paginator(articles, pageSize)  # 创建分页对象
    page_obj = paginator.get_page(pageIndex)  # 获取当前页的数据

    # 将分页后的数据转换为JSON
    articles_data = [
        {
            'no': article.no,
            'title': article.title,
            'author': f"{article.author.first_name}{article.author.last_name}",
            'createTime': article.createTime,
            'updateTime': article.updateTime,
        } for article in page_obj
    ]

    return JsonResponse({
        'message': '获取文章列表成功',
        'data': {'list': articles_data,
                 'total': paginator.count},
        'code': '200'
    }, status=200)


def getDetail(request):
    if request.method != 'GET':
        return JsonResponse({'message': '无效的请求方法', 'code': '405'}, status=405)
    no = request.GET.get('no')
    if not no:
        return JsonResponse({'message': '序号不能为空', 'code': '405'}, status=405)
    articles = UserArticle.objects.all()
    article = articles.filter(no=no).first()
    if article:
        return JsonResponse({
            'message': '获取文章成功',
            'data': {
                'no': article.no,
                'title': article.title,
                'author': f"{article.author.first_name}{article.author.last_name}",
                'createTime': article.createTime,
                'updateTime': article.updateTime,
                'content': article.content,
            },
            'code': '200'
        }, status=200)
    else:
        return JsonResponse({'message': '该文章不存在', 'code': '405'}, status=405)


def delete(request):
    if request.method != 'DELETE':
        return JsonResponse({'message': '无效的请求方法', 'code': '405'}, status=405)
    no = request.GET.get('no')
    if not no:
        return JsonResponse({'message': '序号不能为空', 'code': '400'}, status=400)
    try:
        article = UserArticle.objects.filter(no=no).first()
        if article:
            article.delete()
            return JsonResponse({
                'message': '删除成功',
                'data': {
                    'no': no,
                },
                'code': '200'
            }, status=200)
        else:
            return JsonResponse({'message': '该文章不存在', 'code': '404'}, status=404)
    except Exception as e:
        return JsonResponse({'message': '删除失败: {}'.format(str(e)), 'code': '500'}, status=500)
