from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from goodsTransport.views import PilotViewSet, ShipViewSet, \
  ContractViewSet, ResourceViewSet, ResourceListViewSet, TransactionViewSet

router = routers.DefaultRouter()
router.register(r'pilots', PilotViewSet, basename='pilot')
router.register(r'ships', ShipViewSet, basename='ship')
router.register(r'contracts', ContractViewSet, basename='contract')
router.register(r'resources', ResourceViewSet, basename='resource')
router.register(r'resourcelists', ResourceListViewSet, basename='resourcelist')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
  path('', include(router.urls)),
  path('admin/', admin.site.urls),
  path('', include('goodsTransport.urls'))
]
