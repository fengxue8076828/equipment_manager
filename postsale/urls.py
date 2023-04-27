from django.urls import path
from .views import DeviceSoldCreateView,DeviceOutboundPDFView,DeviceForSaleListView,DeviceSoldUpdateView,OutBoundListView,DeviceSoldListView,DeviceSoldModifyView

app_name = "postsale"
urlpatterns = [
    path("device-sold-create/",DeviceSoldCreateView.as_view(),name="device-sold-create"),
    path("outbound-file/",DeviceOutboundPDFView.as_view(),name="outbound-file"),
    path("device-forsale-list/",DeviceForSaleListView.as_view(),name="device-forsale-list"),
    path("device-sold-update/",DeviceSoldUpdateView.as_view(),name="device-sold-update"),
    path("outbound-list/",OutBoundListView.as_view(),name="outbound-list"),
    path("device-sold-list/",DeviceSoldListView.as_view(),name="device-sold-list"),
    path("device-sold-modify/<device_sold_id>/",DeviceSoldModifyView.as_view(),name="device-sold-modify")
]