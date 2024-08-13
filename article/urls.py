from django.urls import path
import article.views as apiViews

urlpatterns = [
    path('createArticle', apiViews.create),
    path('getPagedList', apiViews.getPagedList),
    path('getDetail', apiViews.getDetail),
]
