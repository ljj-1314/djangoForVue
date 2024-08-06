from django.urls import path
import api.views as apiViews

urlpatterns = [
    path('items/', apiViews.ItemListCreateAPIView.as_view(), name='item-list'),
    path('items/<int:pk>/', apiViews.ItemDetailAPIView.as_view(), name='item-detail'),
    path('register', apiViews.register),
]
