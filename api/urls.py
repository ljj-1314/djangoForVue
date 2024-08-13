from django.urls import path
import api.views as apiViews

urlpatterns = [
    path('register', apiViews.register),
    path('login', apiViews.login),
    path('getUserInfo', apiViews.getUserInfo),
    path('updateUserInfo', apiViews.update_user_info),
    path('upload_avatar', apiViews.upload_avatar, name='upload_avatar'),
]
