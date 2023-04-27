from django.urls import path
from .views import EquipmentListView,EquipmentDeviceListView,EquipmentCreateView,InboundCreateView,EquipmentDetailView,EquipmentUpdateView,EquipmentDeleteView,EquipDeviceInboundPDFView,EquipmentDeviceUpdateView

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
    path('inbound-file/<equipment_id>/<warehouse_id>/<amount>/',EquipDeviceInboundPDFView.as_view(),name="inbound-file")
]