import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import JsonResponse

from image.models import ImageSave
from store.models import StoreType, Store


def create_store_type(request):
    if request.method != 'POST':
        return JsonResponse({'message': '无效的请求方法', 'code': '405'}, status=405)

    try:
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')
        if not title:
            return JsonResponse({'message': '类名不能为空', 'code': '400'}, status=400)
        if not description:
            return JsonResponse({'message': '描述不能为空', 'code': '400'}, status=400)
        store_type = StoreType(title=title, description=description)
        store_type.save()
        return JsonResponse({'message': '类型创建成功', 'data': {'no': store_type.no}, 'code': '200'}, status=200)
    except json.JSONDecodeError as e:
        return JsonResponse({'message': '请求数据格式错误', 'code': '400'}, status=400)
    except IntegrityError as e:
        print('错误1', e)
        return JsonResponse({'message': str(e), 'code': '400'}, status=400)
    except Exception as e:
        print('错误2', e)
        return JsonResponse({'message': str(e), 'code': '500'}, status=500)


def store_type_list(request):
    if request.method != 'GET':
        return JsonResponse({'message': '无效的请求方法', 'code': '405'}, status=405)
    page_index = request.GET.get('pageIndex')
    page_size = request.GET.get('pageSize')
    title = request.GET.get('title')
    if not page_index or not page_size or int(page_size) < 1 or int(page_index) < 1:
        return JsonResponse({'message': '分页数和页码不正确', 'code': '405'}, status=405)
    types = StoreType.objects.all()
    if title:
        types = types.filter(title__icontains=title)
    paginator = Paginator(types, page_size)
    page_obj = paginator.page(page_index)
    data = [
        {
            'no': item.no,
            'title': item.title,
            'description': item.description,
        } for item in page_obj
    ]
    return JsonResponse({'data': {'list': data, 'total': paginator.count}, 'code': '200'}, status=200)


def store_type_detail(request):
    if request.method != 'GET':
        return JsonResponse({'message': '无效的请求方法', 'code': '405'}, status=405)
    no = request.GET.get('no')
    if not no:
        return JsonResponse({'message': '序号不能为空', 'code': '405'}, status=405)
    store_type = StoreType.objects.all().filter(no=no).first()
    if type:
        return JsonResponse({
            'message': '获取成功',
            'data': {
                'no': store_type.no,
                'title': store_type.title,
                'description': store_type.description,
            },
            'code': '200'
        })
    else:
        return JsonResponse({'message': '该类不存在', 'code': '400'}, status=400)


def store_type_update(request):
    if request.method != 'POST':
        return JsonResponse({'message': '无效的请求方法', 'code': '405'}, status=405)
    try:
        data = json.loads(request.body)
        no = data.get('no')
        title = data.get('title')
        description = data.get('description')
        if not no:
            return JsonResponse({'message': '序号不能为空', 'code': '400'}, status=400)
        try:
            types = StoreType.objects.get(no=no)
        except ObjectDoesNotExist:
            return JsonResponse({'message': '不存在该类别，请重试', 'code': '400'}, status=400)
        type_update = StoreType.objects.filter(no=no).update(title=title, description=description)
        if type_update == 1:
            return JsonResponse({'message': '类别编辑成功', 'data': {'no': no}, 'code': '200'}, status=200)
        else:
            return JsonResponse({'message': '类别更新失败', 'code': '400'}, status=400)

    except IntegrityError as e:
        print('错误1', e)
        return JsonResponse({'message': str(e), 'code': '400'}, status=400)
    except Exception as e:
        print('错误2', e)
        return JsonResponse({'message': str(e), 'code': '500'}, status=500)


def store_type_delete(request):
    if request.method != 'DELETE':
        return JsonResponse({'message': '无效的请求方法', 'code': '405'}, status=405)
    no = request.GET.get('no')
    if not no:
        return JsonResponse({'message': '序号不能为空', 'code': '400'}, status=400)
    try:
        store_types = StoreType.objects.filter(no=no).first()
        if store_types:
            store_types.delete()
            return JsonResponse({
                'message': '删除成功',
                'data': {
                    'no': no,
                },
                'code': '200'
            }, status=200)
        else:
            return JsonResponse({'message': '该类别不存在', 'code': '404'}, status=404)
    except Exception as e:
        return JsonResponse({'message': '删除失败: {}'.format(str(e)), 'code': '500'}, status=500)


def create_store(request):
    if request.method != 'POST':
        return JsonResponse({'message': '无效的请求方法', 'code': 405}, status=405)

    try:
        data = json.loads(request.body)
        title = data.get('title')
        value = data.get('value')
        manufacturer = data.get('manufacturer')
        types_nos = data.get('types')  # 这应该是一个包含 storeType 编号的列表

        if not title or not value or not manufacturer or not types_nos:
            return JsonResponse({'message': '必要的字段不能为空', 'code': 400}, status=400)

        # 创建 store 实例
        new_store = Store(title=title, value=value, manufacturer=manufacturer)
        new_store.save()  # 先保存 store 实例

        # 处理多对多关系，绑定多个 storeType
        types = StoreType.objects.filter(no__in=types_nos)
        if not types.exists():
            return JsonResponse({'message': '无效的商品类别', 'code': 400}, status=400)
        new_store.store_type.set(types)  # 设置 ManyToMany 关系

        image_ids = data.get('images', [])
        images = ImageSave.objects.filter(id__in=image_ids)

        if images.exists():
            new_store.images.set(images)

        new_store.save()

        return JsonResponse({'message': '商品创建成功', 'data': {'no': new_store.no}, 'code': 200}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'message': '请求数据格式错误', 'code': 400}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e), 'code': 500}, status=500)


def update_store(request):
    if request.method != 'POST':
        return JsonResponse({'message': '无效的请求方法', 'code': '405'}, status=405)
    try:
        data = json.loads(request.body)
        title = data.get('title')
        no = data.get('no')
        value = data.get('value')
        manufacturer = data.get('manufacturer')
        types_nos = data.get('types')  # 这应该是一个包含 storeType 编号的列表
        image_ids = data.get('images', [])

        if not no:
            return JsonResponse({'message': '序号不能为空', 'code': '400'}, status=400)
        if not title or not value or not manufacturer or not types_nos:
            return JsonResponse({'message': '必要的字段不能为空', 'code': 400}, status=400)

            # 查找对应的 Store 对象
        try:
            store = Store.objects.get(no=no)
        except Store.DoesNotExist:
            return JsonResponse({'message': '不存在该商品，请重试', 'code': '400'}, status=400)

        # 获取有效的 StoreType 和 ImageSave
        types = StoreType.objects.filter(no__in=types_nos)
        if not types.exists():
            return JsonResponse({'message': '无效的商品类别', 'code': 400}, status=400)

        images = ImageSave.objects.filter(id__in=image_ids)

        # 更新 Store 对象
        store.title = title
        store.value = value
        store.manufacturer = manufacturer
        store.save()

        # 更新多对多字段
        store.store_type.set(types)
        store.images.set(images)

        return JsonResponse({'message': '商品编辑成功', 'data': {'no': no}, 'code': '200'}, status=200)

    except IntegrityError as e:
        print('错误1', e)
        return JsonResponse({'message': str(e), 'code': '400'}, status=400)
    except Exception as e:
        print('错误2', e)
        return JsonResponse({'message': str(e), 'code': '500'}, status=500)


def store_delete(request):
    if request.method != 'DELETE':
        return JsonResponse({'message': '无效的请求方法', 'code': '405'}, status=405)
    no = request.GET.get('no')
    if not no:
        return JsonResponse({'message': '序号不能为空', 'code': '400'}, status=400)
    try:
        store_exist = Store.objects.filter(no=no).exists()
        if store_exist:
            store = Store.objects.get(no=no)
            store.store_type.clear()
            store.images.clear()
            store.delete()
            return JsonResponse({
                'message': '删除成功',
                'data': {
                    'no': no,
                },
                'code': '204'
            }, status=204)
        else:
            return JsonResponse({'message': '该商品不存在', 'code': '404'}, status=404)
    except Exception as e:
        return JsonResponse({'message': '删除失败: {}'.format(str(e)), 'code': '500'}, status=500)


def store_list(request):
    if request.method != 'GET':
        return JsonResponse({'message': '无效的请求方法', 'code': '405'}, status=405)
    page_index = request.GET.get('pageIndex')
    page_size = request.GET.get('pageSize')
    # title = request.GET.get('title')
    if not page_index or not page_size or int(page_size) < 1 or int(page_index) < 1:
        return JsonResponse({'message': '分页数和页码不正确', 'code': '405'}, status=405)
    stores = Store.objects.all()
    # if title:
    #     types = types.filter(title__icontains=title)
    paginator = Paginator(stores, page_size)
    page_obj = paginator.page(page_index)
    data = [
        {
            'no': item.no,
            'title': item.title,
            'store_type': [store_type.title for store_type in item.store_type.all()],
            'value': item.value,
            'manufacturer': item.manufacturer,
            'images': [store_image.image.url for store_image in item.images.all()],
        } for item in page_obj
    ]
    return JsonResponse({'data': {'list': data, 'total': paginator.count}, 'code': '200'}, status=200)
