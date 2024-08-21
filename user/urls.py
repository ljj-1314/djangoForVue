from django.urls import path
import user.views as apiViews

urlpatterns = [
    path('register', apiViews.register),
    path('login', apiViews.login),
    path('getUserInfo', apiViews.getUserInfo),
    path('updateUserInfo', apiViews.update_user_info),
]
