from django.urls import path
from .views import EquipmentListView,EquipmentDeviceListView,EquipmentCreateView,InboundCreateView,EquipmentDetailView,EquipmentUpdateView,EquipmentDeleteView,EquipDeviceInboundPDFView,EquipmentDeviceUpdateView,SupplierListView,SupplierCreateView,SupplierUpdateView,SupplierDeleteView,EquipmentDeviceListByWarehouseView

app_name = "presale"
urlpatterns = [
    path('equipment-list/',EquipmentListView.as_view(),name='equipment-list'),
    path('equipment-create/',EquipmentCreateView.as_view(),name="equipment-create"),
    path('equipment-detail/<id>/',EquipmentDetailView.as_view(),name="equipment-detail"),
    path('equipment-update/<int:pk>/',EquipmentUpdateView.as_view(),name="equipment-update"),
    path('equipment-delete/<int:pk>',EquipmentDeleteView.as_view(),name="equipment-delete"),
    path('device-list/',EquipmentDeviceListView.as_view(),name="device-list"),  
    path('inbound-create/',InboundCreateView.as_view(),name="inbound-create"),
    path('device-list/<equipment_id>/',EquipmentDeviceListView.as_view(),name="device-list"),
    path('device-update/<device_id>/',EquipmentDeviceUpdateView.as_view(),name="device-update"),
    path('inbound-file/<equipment_id>/<warehouse_id>/<amount>/<supplier_id>/',EquipDeviceInboundPDFView.as_view(),name="inbound-file"),
    path('supplier-list/',SupplierListView.as_view(),name="supplier-list"),
    path('supplier-create/',SupplierCreateView.as_view(),name="supplier-create"),
    path('supplier-update/<supplier_id>/',SupplierUpdateView.as_view(),name="supplier-update"),
    path('supplier-delete/<int:pk>',SupplierDeleteView.as_view(),name="supplier-delete"),
    path('device-list-by-warehouse/<warehouse_id>/',EquipmentDeviceListByWarehouseView.as_view(),name="device-list-by-warehouse"),
]