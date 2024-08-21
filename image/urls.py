from django.urls import path
import image.views as imageview

urlpatterns = [
    path('imageUpload', imageview.image_upload),

]
