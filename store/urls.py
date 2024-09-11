from django.urls import path
import store.views as apiViews

urlpatterns = [
    path('createStoreType', apiViews.create_store_type),
    path('updateStoreType', apiViews.store_type_update),
    path('storeTypeList', apiViews.store_type_list),
    path('storeTypeDetail', apiViews.store_type_detail),
    path('storeTypeDelete', apiViews.store_type_delete),
    path('createStore', apiViews.create_store),
    path('updateStore', apiViews.update_store),
    path('deleteStore',apiViews.store_delete),
    path('storeList', apiViews.store_list),
]
