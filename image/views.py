import json

from django.db import IntegrityError
from django.http import JsonResponse

from image.models import ImageSave


def image_upload(request):
    if request.method != 'POST':
        return JsonResponse({'message': '无效的请求方法', 'code': '405'}, status=405)

    image_file = request.FILES.get('image_file')
    if not image_file:
        return JsonResponse({'message': '没有上传图片', 'code': '400'}, status=400)

    image_instance = ImageSave(image=image_file)
    image_instance.save()

    # 使用 image_instance.image.url 获取图片的 URL
    return JsonResponse(
        {
            'message': '图片上传成功',
            'data': {
                'id': image_instance.id,  # 如果需要返回 id
                'img': image_instance.image.url,  # 获取图片的 URL
            },
            'code': '200'
        },
        status=200
    )
