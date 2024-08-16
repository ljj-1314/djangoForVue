from django.urls import path
import article.views as apiViews

urlpatterns = [
    path('createArticle', apiViews.create),
    path('updateArticle', apiViews.update),
    path('getPagedList', apiViews.getPagedList),
    path('getDetail', apiViews.getDetail),
    path('deleteArticle', apiViews.delete),
]
